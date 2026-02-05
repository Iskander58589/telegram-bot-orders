"""
Сервис для работы с заказами
"""

from datetime import datetime
from config import PRICES


class OrderService:
    """Сервис для обработки логики заказов"""
    
    # Словарь для хранения заказов в памяти (для MVP)
    orders_storage = {}
    order_counter = 1000
    
    @classmethod
    def calculate_price(cls, work_type: str, urgency: str) -> int:
        """
        Расчет цены заказа
        
        Args:
            work_type: тип работы
            urgency: срочность
            
        Returns:
            Цена в тенге
        """
        if work_type in PRICES:
            price = PRICES[work_type].get(urgency, PRICES[work_type]["standard"])
        else:
            price = PRICES["other"].get(urgency, PRICES["other"]["standard"])
        
        return int(price)
    
    @classmethod
    def create_order(cls, user_id: int, username: str, work_type: str, 
                     urgency: str, details: str, price: int) -> dict:
        """
        Создание нового заказа
        
        Args:
            user_id: ID пользователя
            username: Username пользователя в Telegram
            work_type: тип работы
            urgency: срочность
            details: описание заказа
            price: цена заказа
            
        Returns:
            Словарь с данными заказа
        """
        order_id = cls.order_counter
        cls.order_counter += 1
        
        order = {
            "order_id": order_id,
            "user_id": user_id,
            "username": username,
            "work_type": work_type,
            "urgency": urgency,
            "details": details,
            "price": price,
            "status": "new",
            "created_at": datetime.now().isoformat(),
        }
        
        cls.orders_storage[order_id] = order
        return order
    
    @classmethod
    def get_order(cls, order_id: int) -> dict:
        """
        Получить заказ по ID
        """
        return cls.orders_storage.get(order_id)
    
    @classmethod
    def format_order_for_admin(cls, order: dict) -> str:
        """
        Форматирование заказа для отправки администратору
        Используем простой текст чтобы избежать ошибок Markdown
        """
        work_type_display = {
            "presentation": "Презентация",
            "report": "Доклад",
            "coursework": "Курсовая работа",
            "lab_work": "Практическая работа",
            "other": "Другое"
        }
        
        urgency_display = {
            "urgent": "Срочная",
            "standard": "Стандартная",
            "no_rush": "Не срочная"
        }
        
        message = f"""НОВЫЙ ЗАКАЗ

Клиент: @{order['username']}
User ID: {order['user_id']}
Заказ ID: #{order['order_id']}

ИНФОРМАЦИЯ О ЗАКАЗЕ:
Тип работы: {work_type_display.get(order['work_type'], order['work_type'])}
Срочность: {urgency_display.get(order['urgency'], order['urgency'])}
Цена: {order['price']} тг

ДЕТАЛИ:
{order['details']}

Время заказа: {order['created_at']}
Статус: {order['status']}

---
Работу нужно выполнить и отправить клиенту."""
        return message
    
    @classmethod
    def format_order_summary(cls, order: dict) -> str:
        """
        Форматирование итога заказа для клиента
        """
        work_type_display = {
            "presentation": "Презентация",
            "report": "Доклад",
            "coursework": "Курсовая работа",
            "lab_work": "Практическая работа",
            "other": "Другое"
        }
        
        urgency_display = {
            "urgent": "Срочная",
            "standard": "Стандартная",
            "no_rush": "Не срочная"
        }
        
        message = f"""ВАШ ЗАКАЗ:

Тип работы: {work_type_display.get(order['work_type'], order['work_type'])}
Срочность: {urgency_display.get(order['urgency'], order['urgency'])}
Итоговая цена: {order['price']} тг

Детали:
{order['details']}

Подтвердите или отмените заказ:
"""
        return message
