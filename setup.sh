#!/bin/bash

# Скрипт для развертывания бота на сервере Hetzner
# Запуск: bash setup.sh

echo "🚀 Развертывание бота на Hetzner..."

# Обновляем систему
echo "📦 Обновляем пакеты системы..."
apt update && apt upgrade -y

# Устанавливаем Python и необходимые пакеты
echo "🐍 Устанавливаем Python 3.10+..."
apt install -y python3 python3-pip python3-venv git

# Создаем директорию для бота
echo "📁 Создаем директорию проекта..."
cd /home
mkdir -p telegram-bot
cd telegram-bot

# Клонируем репозиторий из GitHub
echo "📥 Клонируем репозиторий из GitHub..."
# Замените на свой URL репозитория!
git clone https://github.com/YOUR_USERNAME/telegram-bot-orders.git .

# Создаем виртуальное окружение
echo "🔧 Создаем виртуальное окружение..."
python3 -m venv venv
source venv/bin/activate

# Устанавливаем зависимости
echo "📚 Устанавливаем зависимости Python..."
pip install -r requirements.txt

# Создаем .env файл с переменными окружения
echo "🔐 Создаем файл .env..."
cat > .env << EOF
BOT_TOKEN=${BOT_TOKEN}
ADMIN_CHAT_ID=${ADMIN_CHAT_ID}
EOF

chmod 600 .env

# Создаем systemd сервис для автозапуска бота
echo "⚙️ Создаем systemd сервис..."
cat > /etc/systemd/system/telegram-bot.service << EOF
[Unit]
Description=Telegram Orders Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/telegram-bot
Environment="PATH=/home/telegram-bot/venv/bin"
ExecStart=/home/telegram-bot/venv/bin/python3 /home/telegram-bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Перезагружаем systemd
systemctl daemon-reload

# Запускаем сервис
echo "▶️ Запускаем бота..."
systemctl start telegram-bot
systemctl enable telegram-bot

# Проверяем статус
echo "✅ Проверяем статус бота..."
systemctl status telegram-bot

echo "🎉 Развертывание завершено!"
echo "📊 Проверить логи: journalctl -u telegram-bot -f"
