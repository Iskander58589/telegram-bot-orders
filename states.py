"""
FSM состояния для оформления заказа
"""

from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    """Состояния для процесса оформления заказа"""
    
    # Основной процесс заказа
    waiting_for_work_type = State()       # Ожидание выбора типа работы
    waiting_for_urgency = State()         # Ожидание выбора срочности
    waiting_for_details = State()         # Ожидание описания заказа
    waiting_for_confirmation = State()    # Ожидание подтверждения заказа
    waiting_for_payment = State()         # Ожидание подтверждения оплаты


class SupportStates(StatesGroup):
    """Состояния для поддержки"""
    
    waiting_for_message = State()         # Ожидание сообщения от пользователя
    waiting_for_admin_message = State()   # Ожидание сообщения для админа
