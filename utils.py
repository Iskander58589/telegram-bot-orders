"""
Утилиты и вспомогательные функции
"""

import logging
from datetime import datetime


logger = logging.getLogger(__name__)


def get_admin_chat_id_from_message():
    """
    Инструкция для получения ID админ-чата
    """
    instructions = """
    ⚠️ ИНСТРУКЦИЯ ПО ПОЛУЧЕНИЮ ADMIN_CHAT_ID:
    
    1. Создайте ЗАКРЫТУЮ группу в Telegram
    2. Добавьте бота в эту группу (сделайте его администратором)
    3. Отправьте любое сообщение в группу
    4. Откройте терминал и выполните команду:
    
    curl "https://api.telegram.org/bot8283115795:AAHRJHjwXivexbPDH-HZg3ydCahBHlzROyM/getUpdates"
    
    5. Найдите в ответе строку с "chat":{"id":...
    6. ID будет отрицательным числом, например: -1001234567890
    7. Скопируйте это число в config.py переменную ADMIN_CHAT_ID
    
    Если у вас возникли проблемы, проверьте:
    - Бот добавлен в группу?
    - Бот имеет права администратора?
    - Вы используете ЗАКРЫТУЮ группу (не канал)?
    """
    return instructions


def format_order_details_for_display(order: dict) -> str:
    """
    Форматирование деталей заказа для красивого отображения
    """
    work_type_names = {
        "presentation": "📊 Презентация",
        "report": "📝 Доклад",
        "essay": "✍️ Эссе",
        "other": "📚 Другое"
    }
    
    urgency_names = {
        "urgent": "🔥 Срочная",
        "standard": "⏱️ Стандартная",
        "no_rush": "😌 Не срочная"
    }
    
    formatted = f"""
📦 Заказ #{order.get('order_id', '?')}

📋 Тип: {work_type_names.get(order.get('work_type'), '?')}
⏱️ Срочность: {urgency_names.get(order.get('urgency'), '?')}
💰 Сумма: {order.get('price', '?')} тг

📝 Детали:
{order.get('details', 'Нет деталей')}

👤 От: @{order.get('username', '?')}
🔗 ID: {order.get('user_id', '?')}
📅 Дата: {order.get('created_at', '?')}
"""
    return formatted


def log_order(order: dict):
    """
    Логирование заказа
    """
    logger.info(f"New order created: #{order['order_id']} from @{order['username']} ({order['user_id']})")
    logger.info(f"Order type: {order['work_type']}, Urgency: {order['urgency']}, Price: {order['price']}")


def validate_price(price: int) -> bool:
    """
    Валидация цены
    """
    if price <= 0:
        logger.warning(f"Invalid price: {price}")
        return False
    if price > 999999:
        logger.warning(f"Price too high: {price}")
        return False
    return True


def get_current_timestamp() -> str:
    """
    Получить текущее время в красивом формате
    """
    return datetime.now().strftime("%d.%m.%Y %H:%M:%S")


# Полезные константы

WORK_TYPE_EMOJIS = {
    "presentation": "📊",
    "report": "📝",
    "essay": "✍️",
    "other": "📚"
}

URGENCY_EMOJIS = {
    "urgent": "🔥",
    "standard": "⏱️",
    "no_rush": "😌"
}

BUTTON_EMOJIS = {
    "confirm": "✅",
    "cancel": "❌",
    "order": "📦",
    "support": "❓",
    "payment": "💳",
    "menu": "🏠"
}
