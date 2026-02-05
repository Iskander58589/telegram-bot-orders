"""
Клавиатуры для бота
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    Главное меню с основными опциями
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Заказать")],
            [KeyboardButton(text="❓ Поддержка"), KeyboardButton(text="💳 Способы оплаты")],
        ],
        resize_keyboard=True,
    )
    return keyboard


def get_work_type_keyboard() -> InlineKeyboardMarkup:
    """
    Выбор типа работы
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Презентация", callback_data="work_type_presentation")],
            [InlineKeyboardButton(text="📝 Доклад", callback_data="work_type_report")],
            [InlineKeyboardButton(text="📖 Курсовой", callback_data="work_type_coursework")],
            [InlineKeyboardButton(text="📋 Отчетное задание", callback_data="work_type_lab_work")],
            [InlineKeyboardButton(text="📚 Другое", callback_data="work_type_other")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_order")],
        ]
    )
    return keyboard


def get_urgency_keyboard() -> InlineKeyboardMarkup:
    """
    Выбор срочности выполнения
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔥 Срочная", callback_data="urgency_urgent")],
            [InlineKeyboardButton(text="⏱️ Стандартная", callback_data="urgency_standard")],
            [InlineKeyboardButton(text="😌 Не срочная", callback_data="urgency_no_rush")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_order")],
        ]
    )
    return keyboard


def get_confirmation_keyboard() -> InlineKeyboardMarkup:
    """
    Подтверждение заказа
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_order")],
            [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_order")],
        ]
    )
    return keyboard


def get_payment_keyboard() -> InlineKeyboardMarkup:
    """
    Кнопка подтверждения оплаты
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Я оплатил", callback_data="payment_confirmed")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_order")],
        ]
    )
    return keyboard


def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Кнопка возврата в главное меню
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠 В главное меню", callback_data="back_to_menu")],
        ]
    )
    return keyboard


def get_support_keyboard() -> ReplyKeyboardMarkup:
    """
    Выбор типа поддержки
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❓ Вопрос")],
            [KeyboardButton(text="🏠 В меню")],
        ],
        resize_keyboard=True,
    )
    return keyboard
