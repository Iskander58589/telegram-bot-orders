"""
Обработчики команд /start, главного меню и поддержки
"""

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config import MESSAGES, PAYMENT_DETAILS, ADMIN_CHAT_ID
from keyboards import get_main_menu_keyboard, get_back_to_menu_keyboard, get_support_keyboard
from states import OrderStates, SupportStates

router = Router()


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    """
    Обработчик команды /start
    """
    await state.clear()
    
    await message.answer(
        MESSAGES["welcome"],
        reply_markup=get_main_menu_keyboard()
    )


@router.message(F.text == "📦 Заказать")
async def start_order(message: Message, state: FSMContext):
    """
    Начало процесса заказа
    """
    await state.set_state(OrderStates.waiting_for_work_type)
    
    from keyboards import get_work_type_keyboard
    
    await message.answer(
        MESSAGES["order_type"],
        reply_markup=get_work_type_keyboard()
    )


@router.message(F.text == "❓ Поддержка")
async def support_menu(message: Message, state: FSMContext):
    """
    Меню поддержки - показываем две опции
    """
    await state.clear()
    
    await message.answer(
        "💬 ПОДДЕРЖКА\n\nВыберите что вам нужно:",
        reply_markup=get_support_keyboard()
    )


@router.message(F.text == "❓ Вопрос")
async def support_question(message: Message, state: FSMContext):
    """
    Режим вопроса в поддержку
    """
    await state.set_state(SupportStates.waiting_for_message)
    
    await message.answer(
        MESSAGES["support_instruction"]
    )


@router.message(F.text == "🏠 В меню")
async def back_to_main_menu(message: Message, state: FSMContext):
    """
    Возврат в главное меню
    """
    await state.clear()
    
    await message.answer(
        MESSAGES["welcome"],
        reply_markup=get_main_menu_keyboard()
    )


@router.message(Command("support"))
async def support_command(message: Message):
    """
    Команда /support - информация об администраторе
    """
    support_info = """
📞 СЛУЖБА ПОДДЕРЖКИ

Если у вас возникли какие-либо проблемы или вопросы, вы можете связаться с администратором напрямую:

👤 Администратор: @levigne

Напишите ему личное сообщение с описанием вашей проблемы, и администратор обязательно вам поможет!

🕐 Обычно отвечаем в течение 1-2 часов.

Спасибо за обращение! 😊
"""
    
    await message.answer(
        support_info,
        reply_markup=get_main_menu_keyboard()
    )


@router.message(F.text == "💳 Способы оплаты")
async def payment_methods(message: Message, state: FSMContext):
    """
    Показать способы оплаты
    """
    await state.clear()
    
    await message.answer(
        f"💳 ДОСТУПНЫЕ СПОСОБЫ ОПЛАТЫ:\n\n{PAYMENT_DETAILS}",
        reply_markup=get_back_to_menu_keyboard()
    )


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    """
    Возврат в главное меню
    """
    await state.clear()
    
    await callback.message.answer(
        MESSAGES["welcome"],
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()


@router.message(SupportStates.waiting_for_message)
async def receive_support_message(message: Message, state: FSMContext, bot: Bot):
    """
    Получение вопроса в поддержку
    Отправляет сообщение в админ-чат
    """
    user_id = message.from_user.id
    username = message.from_user.username or "Без username"
    user_name = message.from_user.first_name or "Пользователь"
    
    # Форматируем сообщение для администратора (без сложного форматирования чтобы избежать ошибок)
    support_message = f"""❓ НОВЫЙ ВОПРОС ПОДДЕРЖКИ

От: @{username} ({user_name})
User ID: {user_id}

ВОПРОС:
{message.text}"""
    
    # Отправляем в админ-чат
    try:
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=support_message
        )
        print(f"[✅] Вопрос поддержки отправлен в админ-чат успешно")
    except Exception as e:
        print(f"[❌] Ошибка при отправке вопроса поддержки в админ-чат: {e}")
        print(f"[❌] ADMIN_CHAT_ID: {ADMIN_CHAT_ID}")
    
    await state.clear()
    
    await message.answer(
        MESSAGES["support_received"],
        reply_markup=get_main_menu_keyboard()
    )


# ========== ОТЛАДОЧНЫЕ КОМАНДЫ ==========

@router.message(Command("debug_orders"))
async def debug_orders(message: Message):
    """Показывает все заказы в хранилище"""
    from order_service import OrderService
    
    orders = OrderService.orders_storage
    
    if not orders:
        await message.answer("❌ Нет заказов в хранилище")
        return
    
    response = f"📦 Всего заказов: {len(orders)}\n\n"
    
    for order_id, order in orders.items():
        response += f"• Заказ #{order_id}: @{order['username']} - {order['status']}\n"
    
    await message.answer(response)


@router.message(Command("debug_admin_id"))
async def debug_admin_id(message: Message):
    """Показывает ID текущего чата"""
    await message.answer(f"ID этого чата: `{message.chat.id}`")


@router.message(Command("debug_admin_chat_id"))
async def debug_admin_chat_config(message: Message):
    """Показывает ADMIN_CHAT_ID из конфига"""
    await message.answer(f"ADMIN_CHAT_ID из config.py: `{ADMIN_CHAT_ID}`")
