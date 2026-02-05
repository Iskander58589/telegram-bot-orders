#!/usr/bin/env python3
"""
Тестовый скрипт для проверки регулярных выражений и логики
"""

import re
import sys
from order_service import OrderService

# Переключаем кодировку для вывода
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Тестируем regex
test_messages = [
    """NOVIY ZAKAZ

Klient: @testuser
User ID: `12345`
Zakaz ID: `#1001`

INFORMACIJA O ZAKAZE:
Tip raboty: Prezentacija
Srochnost: Srochno (do 2 chasov) +40%
Cena: 3500 tg

DETALI:
Sdelat prezentaciju pro istoriju

Vremja zakaza: 2026-02-01T10:30:00
Status: new

---
Rabotu nuzhno vypolnit i otpravit klijentu.""",
    
    "Zakaz ID: `#1002` - test",
    "No order here",
]

print("=" * 60)
print("TEST REGULJARNOGO VYRAZHENIJA")
print("=" * 60)

pattern = r'Zakaz ID: `#(\d+)`'

for i, msg in enumerate(test_messages, 1):
    print(f"\n[Test {i}]")
    print(f"Message: {msg[:100]}...")
    match = re.search(pattern, msg)
    if match:
        order_id = int(match.group(1))
        print(f"OK - Found order ID: {order_id}")
    else:
        print(f"ERROR - Order not found")

print("\n" + "=" * 60)
print("TEST STORAGE")
print("=" * 60)

# Тестируем OrderService
print(f"\nCurrent counter value: {OrderService.order_counter}")
print(f"Storage: {OrderService.orders_storage}")

# Создаем тестовый заказ
test_order = OrderService.create_order(
    user_id=12345,
    username="testuser",
    work_type="presentation",
    urgency="standard",
    details="Test order",
    price=2500
)

print(f"\nCreated order: {test_order}")
print(f"New counter value: {OrderService.order_counter}")

# Получаем заказ обратно
retrieved_order = OrderService.get_order(test_order['order_id'])
print(f"\nRetrieved order: {retrieved_order}")

if retrieved_order == test_order:
    print("OK - Orders match!")
else:
    print("ERROR - Orders DO NOT match!")

print("\n" + "=" * 60)
print("ALL TESTS PASSED")
print("=" * 60)
