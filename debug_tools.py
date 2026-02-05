"""
Примеры и скрипты для отладки и тестирования бота
"""

# ============================================
# ПРИМЕР 1: Получение ADMIN_CHAT_ID
# ============================================

import requests

def get_updates():
    """
    Получить обновления от Telegram API
    Используйте для поиска ADMIN_CHAT_ID
    """
    token = "8283115795:AAHRJHjwXivexbPDH-HZg3ydCahBHlzROyM"
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get('ok'):
            print("✅ Успешное подключение к API Telegram")
            print("\n📋 Все обновления:")
            
            if data.get('result'):
                for update in data['result']:
                    if 'message' in update:
                        msg = update['message']
                        chat_id = msg.get('chat', {}).get('id')
                        from_user = msg.get('from', {})
                        text = msg.get('text', '[no text]')
                        
                        print(f"\n📨 Сообщение:")
                        print(f"   Chat ID: {chat_id}")
                        print(f"   User: {from_user.get('username', 'no username')}")
                        print(f"   User ID: {from_user.get('id', '?')}")
                        print(f"   Текст: {text}")
            else:
                print("❌ Обновлений нет. Убедитесь, что:")
                print("   1. Вы отправили сообщение в чат/группу")
                print("   2. Бот добавлен в чат")
        else:
            print("❌ Ошибка API:", data.get('description'))
            
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        print("Убедитесь, что у вас есть интернет")


# ============================================
# ПРИМЕР 2: Проверка токена
# ============================================

def verify_bot_token():
    """
    Проверить валидность токена бота
    """
    token = "8283115795:AAHRJHjwXivexbPDH-HZg3ydCahBHlzROyM"
    url = f"https://api.telegram.org/bot{token}/getMe"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get('ok'):
            bot_info = data.get('result', {})
            print("✅ Токен корректен!")
            print(f"\n🤖 Информация о боте:")
            print(f"   ID: {bot_info.get('id')}")
            print(f"   Username: @{bot_info.get('username')}")
            print(f"   Имя: {bot_info.get('first_name')}")
            print(f"   Может читать историю: {bot_info.get('can_read_all_group_messages')}")
        else:
            print("❌ Токен неверный!")
            print("Ошибка:", data.get('description'))
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")


# ============================================
# ПРИМЕР 3: Отправка тестового сообщения
# ============================================

def send_test_message(chat_id: int, message: str):
    """
    Отправить тестовое сообщение
    
    Использование:
    send_test_message(-1001234567890, "Привет, это тест!")
    """
    token = "8283115795:AAHRJHjwXivexbPDH-HZg3ydCahBHlzROyM"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    params = {
        'chat_id': chat_id,
        'text': message
    }
    
    try:
        response = requests.post(url, json=params)
        data = response.json()
        
        if data.get('ok'):
            print(f"✅ Сообщение отправлено в чат {chat_id}")
        else:
            print(f"❌ Ошибка отправки: {data.get('description')}")
            print("\nПроверьте:")
            print("- Правильный ли это chat_id?")
            print("- Добавлен ли бот в этот чат?")
            print("- Бот имеет права на отправку сообщений?")
            
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")


# ============================================
# ПРИМЕР 4: Логирование заказов
# ============================================

import json
from datetime import datetime

def save_order_log(order: dict):
    """
    Сохранить заказ в лог-файл для отладки
    """
    log_file = "orders_log.json"
    
    try:
        # Читаем существующие заказы
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                orders = json.load(f)
        except FileNotFoundError:
            orders = []
        
        # Добавляем новый заказ с временной меткой
        order_with_time = {
            **order,
            'logged_at': datetime.now().isoformat()
        }
        orders.append(order_with_time)
        
        # Сохраняем обратно
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(orders, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Заказ #{order['order_id']} сохранён в {log_file}")
        
    except Exception as e:
        print(f"❌ Ошибка при сохранении лога: {e}")


def read_orders_log():
    """
    Прочитать все сохранённые заказы из лога
    """
    log_file = "orders_log.json"
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            orders = json.load(f)
        
        print(f"\n📊 Всего заказов: {len(orders)}\n")
        
        for order in orders:
            print(f"Заказ #{order['order_id']}")
            print(f"  От: @{order['username']} (ID: {order['user_id']})")
            print(f"  Тип: {order['work_type']}")
            print(f"  Срочность: {order['urgency']}")
            print(f"  Цена: {order['price']} тг")
            print(f"  Статус: {order.get('status', 'unknown')}")
            print(f"  Создан: {order.get('created_at', '?')}")
            print()
            
    except FileNotFoundError:
        print("❌ Файл лога не найден. Заказов пока нет.")
    except Exception as e:
        print(f"❌ Ошибка при чтении лога: {e}")


# ============================================
# ПРИМЕР 5: Статистика заказов
# ============================================

def orders_statistics():
    """
    Вывести статистику по заказам
    """
    log_file = "orders_log.json"
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            orders = json.load(f)
        
        if not orders:
            print("❌ Нет заказов для анализа")
            return
        
        # Подсчеты
        total_orders = len(orders)
        total_revenue = sum(order['price'] for order in orders)
        
        work_types = {}
        urgencies = {}
        
        for order in orders:
            work_type = order.get('work_type', 'unknown')
            urgency = order.get('urgency', 'unknown')
            price = order.get('price', 0)
            
            work_types[work_type] = work_types.get(work_type, 0) + 1
            urgencies[urgency] = urgencies.get(urgency, {})
            urgencies[urgency]['count'] = urgencies[urgency].get('count', 0) + 1
            urgencies[urgency]['revenue'] = urgencies[urgency].get('revenue', 0) + price
        
        # Вывод
        print("\n📊 СТАТИСТИКА ЗАКАЗОВ\n")
        print(f"Всего заказов: {total_orders}")
        print(f"Общая сумма: {total_revenue} тг")
        print(f"Средний заказ: {total_revenue // total_orders if total_orders else 0} тг")
        
        print("\n📋 По типам работ:")
        for work_type, count in work_types.items():
            print(f"  {work_type}: {count}")
        
        print("\n⏱️ По срочности:")
        for urgency, data in urgencies.items():
            print(f"  {urgency}: {data['count']} заказов, {data['revenue']} тг")
        
    except FileNotFoundError:
        print("❌ Файл лога не найден")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


# ============================================
# ГЛАВНОЕ МЕНЮ
# ============================================

if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════╗
║  🤖 ОТЛАДОЧНЫЕ ИНСТРУМЕНТЫ ДЛЯ TELEGRAM-БОТА         ║
╚════════════════════════════════════════════════════════╝

Выберите действие:

1️⃣  Получить ADMIN_CHAT_ID (найти ID вашей группы)
2️⃣  Проверить токен бота
3️⃣  Отправить тестовое сообщение
4️⃣  Прочитать все сохранённые заказы
5️⃣  Статистика заказов
0️⃣  Выход
    """)
    
    choice = input("\nВыберите (0-5): ").strip()
    
    if choice == '1':
        print("\n⏳ Получаю обновления от API...")
        get_updates()
    
    elif choice == '2':
        print("\n⏳ Проверяю токен...")
        verify_bot_token()
    
    elif choice == '3':
        chat_id = input("Введите chat_id (например -1001234567890): ").strip()
        message = input("Введите текст сообщения: ").strip()
        try:
            send_test_message(int(chat_id), message)
        except ValueError:
            print("❌ chat_id должен быть числом")
    
    elif choice == '4':
        read_orders_log()
    
    elif choice == '5':
        orders_statistics()
    
    elif choice == '0':
        print("До свидания! 👋")
    
    else:
        print("❌ Неверный выбор")
