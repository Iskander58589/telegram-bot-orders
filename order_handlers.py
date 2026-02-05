"""
Обработчики процесса оформления заказа (работают с FSM)
"""

import re
import traceback
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from config import MESSAGES, PAYMENT_DETAILS, ADMIN_CHAT_ID
from keyboards import (
    get_urgency_keyboard, 
    get_confirmation_keyboard,
    get_payment_keyboard,
    get_main_menu_keyboard,
)
from states import OrderStates
from order_service import OrderService

router = Router()


# ========== Выбор типа работы ==========

@router.callback_query(F.data.startswith("work_type_"))
async def select_work_type(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик выбора типа работы
    """
    work_type = callback.data.replace("work_type_", "")
    
    # Сохраняем выбор в контекст
    await state.update_data(work_type=work_type)
    
    # Переходим к выбору срочности
    await state.set_state(OrderStates.waiting_for_urgency)
    
    await callback.message.edit_text(
        MESSAGES["urgency"],
        reply_markup=get_urgency_keyboard()
    )
    await callback.answer()


# ========== Выбор срочности ==========

@router.callback_query(F.data.startswith("urgency_"))
async def select_urgency(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик выбора срочности
    """
    urgency = callback.data.replace("urgency_", "")
    
    # Сохраняем выбор в контекст
    await state.update_data(urgency=urgency)
    
    # Переходим к вводу деталей
    await state.set_state(OrderStates.waiting_for_details)
    
    await callback.message.edit_text(
        MESSAGES["details"]
    )
    await callback.answer()


# ========== Ввод деталей заказа ==========

@router.message(OrderStates.waiting_for_details)
async def receive_details(message: Message, state: FSMContext):
    """
    Получение деталей заказа
    """
    details = message.text
    
    # Получаем данные из контекста
    data = await state.get_data()
    work_type = data.get("work_type")
    urgency = data.get("urgency")
    
    # Рассчитываем цену
    price = OrderService.calculate_price(work_type, urgency)
    
    # Сохраняем данные в контекст
    await state.update_data(
        details=details,
        price=price
    )
    
    # Переходим к подтверждению
    await state.set_state(OrderStates.waiting_for_confirmation)
    
    # Показываем итог заказа
    order_summary = OrderService.format_order_summary({
        "work_type": work_type,
        "urgency": urgency,
        "price": price,
        "details": details
    })
    
    await message.answer(
        order_summary,
        reply_markup=get_confirmation_keyboard(),
        parse_mode="Markdown"
    )


# ========== Подтверждение или отмена заказа ==========

@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    """
    Подтверждение заказа и переход к оплате
    """
    data = await state.get_data()
    
    # Переходим к оплате
    await state.set_state(OrderStates.waiting_for_payment)
    
    # Показываем инструкции по оплате
    payment_message = MESSAGES["payment_instruction"].format(
        payment_details=PAYMENT_DETAILS,
        order_id="9999"  # Временный ID (будет заменён на реальный)
    )
    
    await callback.message.edit_text(
        payment_message,
        reply_markup=get_payment_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "cancel_order")
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    """
    Отмена заказа
    """
    await state.clear()
    
    await callback.message.answer(
        "❌ Заказ отменён.\n\n" + MESSAGES["welcome"],
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()


# ========== Подтверждение оплаты ==========

@router.callback_query(F.data == "payment_confirmed")
async def payment_confirmed(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Пользователь подтвердил оплату
    Заказ отправляется администратору
    """
    data = await state.get_data()
    
    # Получаем данные пользователя
    user_id = callback.from_user.id
    username = callback.from_user.username or "Без username"
    
    print(f"\n[📦 НОВЫЙ ЗАКАЗ]")
    print(f"  Клиент: @{username} (ID: {user_id})")
    
    # Создаём заказ
    order = OrderService.create_order(
        user_id=user_id,
        username=username,
        work_type=data.get("work_type"),
        urgency=data.get("urgency"),
        details=data.get("details"),
        price=data.get("price")
    )
    
    print(f"  Заказ ID: #{order['order_id']}")
    print(f"  Тип: {data.get('work_type')}")
    print(f"  Цена: {order['price']} тг")
    
    # Отправляем уведомление администратору
    admin_message = OrderService.format_order_for_admin(order)
    
    # Создаём кнопки для админ-чата
    admin_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="✅ Принять заказ",
                callback_data=f"accept_order_{user_id}_{order['order_id']}"
            )],
            [InlineKeyboardButton(
                text="❌ Отклонить",
                callback_data=f"reject_order_{user_id}_{order['order_id']}"
            )],
        ]
    )
    
    print(f"\n[📤 ОТПРАВКА В АДМИН-ЧАТ]")
    print(f"  Целевой чат ID: {ADMIN_CHAT_ID}")
    
    try:
        msg = await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_message,
            reply_markup=admin_keyboard
        )
        print(f"  ✅ УСПЕШНО отправлено!")
        print(f"  Message ID в чате: {msg.message_id}")
        print(f"[✅] Заказ #{order['order_id']} отправлен в админ-чат успешно\n")
    except Exception as e:
        print(f"  ❌ ОШИБКА!")
        print(f"[❌] КРИТИЧЕСКАЯ ОШИБКА при отправке заказа в админ-чат!")
        print(f"[❌] Ошибка: {e}")
        print(f"[❌] Тип ошибки: {type(e).__name__}")
        print(f"[❌] ADMIN_CHAT_ID из config.py: {ADMIN_CHAT_ID}")
        print(f"[❌] Заказ ID: {order['order_id']}")
        print(f"[❌] User ID: {user_id}")
        
        # Попробуем отправить сообщение клиенту что произошла ошибка
        try:
            await callback.message.edit_text(
                f"""
❌ ОШИБКА ПРИ ОТПРАВКЕ ЗАКАЗА

Ваш заказ не был отправлен администратору.
Это может быть проблема на сервере.

Код ошибки: {type(e).__name__}
Сообщение: {str(e)[:100]}

Пожалуйста, обратитесь к администратору: @levigne

❓ Ваш заказ ID: #{order['order_id']}
"""
            )
        except:
            pass
    
    # Отправляем подтверждение пользователю - ОБРАБОТКА ПЛАТЕЖА
    await callback.message.edit_text(
        """
⏳ ОБРАБОТКА ПЛАТЕЖА

Спасибо за оплату! 🙏

Ваш платеж проверяется...
Администратор проверит платёж и подтвердит ваш заказ.

📱 Дождитесь уведомления от бота ✅
        """
    )
    
    await state.clear()
    await callback.answer()


# ========== Обработчики админ-команд ==========

@router.callback_query(F.data.startswith("accept_order_"))
async def accept_order(callback: CallbackQuery, bot: Bot):
    """
    Администратор принял заказ
    """
    # Парсим callback_data: accept_order_USER_ID_ORDER_ID
    parts = callback.data.split("_")
    user_id = int(parts[2])
    order_id = int(parts[3])
    
    # Получаем заказ
    order = OrderService.get_order(order_id)
    
    if order:
        # Отправляем сообщение клиенту
        try:
            await bot.send_message(
                chat_id=user_id,
                text=f"""
✅ ЗАКАЗ ПРИНГТ И ПОДТВЕРЖДЕН!

Спасибо за заказ! 🎉

📋 Номер вашего заказа: #{order['order_id']}
💰 Сумма: {order['price']} тг

🔄 Статус: Работа в процессе ⏳

Мы выполним вашу работу в установленный срок и отправим результат.

Спасибо за доверие! 😊
"""
            )
        except Exception as e:
            print(f"Ошибка при отправке клиенту: {e}")
        
        # Обновляем статус заказа
        order['status'] = 'accepted'
        
        # Обновляем сообщение в админ-чате
        updated_message = OrderService.format_order_for_admin(order)
        updated_message += "\n\n✅ ЗАКАЗ ПРИНГТ АДМИНИСТРАТОРОМ"
        
        try:
            await callback.message.edit_text(
                updated_message
            )
        except Exception as e:
            print(f"Ошибка при обновлении сообщения: {e}")
    
    await callback.answer("✅ Заказ принят! Клиент уведомлен.", show_alert=True)


@router.callback_query(F.data.startswith("reject_order_"))
async def reject_order(callback: CallbackQuery, bot: Bot):
    """
    Администратор отклонил заказ
    """
    # Парсим callback_data: reject_order_USER_ID_ORDER_ID
    parts = callback.data.split("_")
    user_id = int(parts[2])
    order_id = int(parts[3])
    
    # Получаем заказ
    order = OrderService.get_order(order_id)
    
    if order:
        # Отправляем сообщение клиенту
        try:
            await bot.send_message(
                chat_id=user_id,
                text=f"""
❌ ЗАКАЗ ОТКЛОНЕН

К сожалению, мы не можем выполнить ваш заказ.

📋 Номер заказа: #{order['order_id']}

Пожалуйста, свяжитесь с нами через кнопку "Поддержка" для получения дополнительной информации.

Спасибо за понимание! 😊
""",
            )
        except Exception as e:
            print(f"Ошибка при отправке клиенту: {e}")
        
        # Обновляем статус заказа
        order['status'] = 'rejected'
        
        # Обновляем сообщение в админ-чате
        updated_message = OrderService.format_order_for_admin(order)
        updated_message += "\n\n❌ ЗАКАЗ ОТКЛОНЕН АДМИНИСТРАТОРОМ"
        
        try:
            await callback.message.edit_text(
                updated_message
            )
        except Exception as e:
            print(f"Ошибка при обновлении сообщения: {e}")
    
    await callback.answer("❌ Заказ отклонен! Клиент уведомлен.", show_alert=True)


# ========== Отправка результата клиенту ==========

@router.message(F.chat.id == int(ADMIN_CHAT_ID))
async def handle_admin_message(message: Message, bot: Bot):
    """
    Обработчик сообщений в админ-чате
    Если это ответ на сообщение заказа - пересылает результат клиенту
    """
    print(f"\n[ADMIN_HANDLER] === ПОЛУЧЕНО СООБЩЕНИЕ В АДМИН-ЧАТЕ ===")
    print(f"[ADMIN_HANDLER] chat_id: {message.chat.id}")
    print(f"[ADMIN_HANDLER] ADMIN_CHAT_ID: {ADMIN_CHAT_ID}")
    print(f"[ADMIN_HANDLER] Match: {message.chat.id == int(ADMIN_CHAT_ID)}")
    
    # Проверяем есть ли reply_to_message
    if not message.reply_to_message:
        print(f"[ADMIN_HANDLER] Нет reply_to_message, пропускаем")
        return
    
    print(f"[ADMIN_HANDLER] Найден reply_to_message")
    
    # Пытаемся найти номер заказа в оригинальном сообщении
    original_text = message.reply_to_message.text or ""
    
    print(f"[ADMIN_HANDLER] Текст оригинального сообщения (первые 200 символов):")
    print(f"[ADMIN_HANDLER] {original_text[:200]}")
    
    # Ищем паттерн "📦 Заказ ID: #1001" или "Заказ ID: `#1001`"
    match = re.search(r'Заказ ID:.*?#(\d+)', original_text)
    
    if not match:
        print(f"[ADMIN_HANDLER] Паттерн не найден, пропускаем")
        return
    
    order_id = int(match.group(1))
    print(f"[ADMIN_HANDLER] Найден заказ ID: {order_id}")
    
    order = OrderService.get_order(order_id)
    
    if not order:
        print(f"[ADMIN_HANDLER] Заказ #{order_id} не найден в storage")
        return
    
    user_id = order['user_id']
    print(f"[ADMIN_HANDLER] Отправляю результат пользователю: {user_id}")
    
    # Отправляем сообщение/файл клиенту
    try:
        sent_something = False
        
        # Пересылаем файлы если они есть
        if message.document:
            print(f"[ADMIN_HANDLER] Отправляю документ")
            await bot.send_document(
                chat_id=user_id,
                document=message.document.file_id,
                caption=f"✅ ВОТ ВАШ ЗАКАЗ!\n\nНомер заказа: #{order_id}\n\n{message.caption or ''}"
            )
            sent_something = True
        elif message.photo:
            print(f"[ADMIN_HANDLER] Отправляю фото")
            await bot.send_photo(
                chat_id=user_id,
                photo=message.photo[-1].file_id,
                caption=f"✅ ВОТ ВАШ ЗАКАЗ!\n\nНомер заказа: #{order_id}\n\n{message.caption or ''}"
            )
            sent_something = True
        elif message.text:
            print(f"[ADMIN_HANDLER] Отправляю текст")
            # Отправляем текстовый результат
            await bot.send_message(
                chat_id=user_id,
                text=f"""✅ ВОТ ВАШ ЗАКАЗ!

Номер заказа: #{order_id}

📏 РЕЗУЛЬТАТ:
{message.text}

Спасибо за обращение! 😊"""
            )
            sent_something = True
        else:
            print(f"[ADMIN_HANDLER] Сообщение не содержит файл, фото или текст")
            return
        
        if sent_something:
            # Отправляем подтверждение в админ-чат
            print(f"[ADMIN_HANDLER] Отправляю подтверждение в админ-чат")
            await message.reply(
                f"✅ Результат отправлен клиенту (@{order['username']})!"
            )
            print(f"[ADMIN_HANDLER] === УСПЕШНО ЗАВЕРШЕНО ===\n")
        
    except Exception as e:
        print(f"[ADMIN_HANDLER] Ошибка при отправке результата: {e}")
        traceback.print_exc()
        await message.reply(
            f"❌ Ошибка: {str(e)}"
        )


# ========== Логирование всех сообщений для отладки ==========

@router.message(F.chat.id == int(ADMIN_CHAT_ID))
async def log_admin_messages(message: Message):
    """Логирует все сообщения в админ-чате для отладки"""
    print(f"[LOG_ADMIN] Сообщение в админ-чате:")
    print(f"  - chat_id: {message.chat.id}")
    print(f"  - ADMIN_CHAT_ID: {ADMIN_CHAT_ID}")
    print(f"  - Match: {message.chat.id == int(ADMIN_CHAT_ID)}")
    print("")
