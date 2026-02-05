#!/usr/bin/env python3
"""
Скрипт для проверки текущего ADMIN_CHAT_ID в config.py
"""

from config import ADMIN_CHAT_ID

print("=" * 60)
print("ПРОВЕРКА ADMIN_CHAT_ID")
print("=" * 60)
print(f"\nАДМИН-ЧАТ ID из config.py: {ADMIN_CHAT_ID}")
print(f"Тип данных: {type(ADMIN_CHAT_ID)}")
print(f"\nЭто ID вашей группы где бот должен отправлять заказы.")
print("\nЕсли заказы не приходят у друга, попросите его:")
print("  1. Напишите боту: /debug_admin_chat_id")
print("  2. Сравните его число с вашим числом выше")
print("  3. Если разные - значит у вас разные админ-чаты!")
print("=" * 60)
