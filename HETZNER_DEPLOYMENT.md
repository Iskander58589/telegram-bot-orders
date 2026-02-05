# 🚀 Гайд по развертыванию бота на Hetzner с GitHub

## 📋 Полный процесс (от и до)

### **ЧАСТЬ 1: ПОДГОТОВКА (Локально на твоем ПК)**

#### Шаг 1.1: Создаем GitHub репозиторий

1. Идешь на [github.com](https://github.com)
2. Нажимаешь **"New"** (создать новый репозиторий)
3. Называешь: `telegram-bot-orders` (или как хочешь)
4. **Выбираешь "Private"** (приватный!) - чтобы никто не видел токены
5. Нажимаешь **"Create repository"**

#### Шаг 1.2: Инициализируем Git локально

```bash
# Открываешь PowerShell в папке бота
cd c:\Users\ASUS\Videos\.gallery\4e2e315c-1878-42fb-8de7-c57a9b83f6dc\bot677

# Инициализируем Git
git init

# Добавляем все файлы КРОМЕ .env (он в .gitignore)
git add .

# Коммитим
git commit -m "Initial commit: telegram orders bot"

# Добавляем удаленный репозиторий (замени USERNAME и REPO)
git remote add origin https://github.com/YOUR_USERNAME/telegram-bot-orders.git

# Переименовываем главную ветку
git branch -M main

# Пушим в GitHub
git push -u origin main
```

#### Шаг 1.3: Добавляем GitHub Secrets (для скрытых переменных)

**Почему это нужно?** GitHub Action будет автоматически развертывать новый код на сервер, но он не должен знать твой токен!

1. Идешь в настройки репозитория: **Settings → Secrets and variables → Actions**
2. Нажимаешь **"New repository secret"**
3. Добавляешь два секрета:

```
Name: BOT_TOKEN
Value: 8283115795:AAHRJHjwXivexbPDH-HZg3ydCahBHlzROyM

Name: ADMIN_CHAT_ID  
Value: -1003898978688
```

---

### **ЧАСТЬ 2: HETZNER СЕРВЕР**

#### Шаг 2.1: Регистрируешься и создаешь сервер

1. Идешь на [hetzner.com](https://www.hetzner.com)
2. **Sign Up** → Регистрируешься
3. В консоли нажимаешь **"Create Server"** (или CloudServer)
4. Выбираешь:
   - **Локация:** Frankfurt или Nuremberg (Европа, близко)
   - **Тип:** Ubuntu 22.04 LTS (самая популярная)
   - **Ресурсы:** CX11 или CX21 (для бота достаточно, от €3.5/месяц)
   - **SSH Key:** Генерируешь новый или загружаешь свой

#### Шаг 2.2: Генерируем SSH ключ (если его нет)

**На Windows (PowerShell):**

```powershell
# Создаешь SSH ключ
ssh-keygen -t rsa -b 4096 -f $env:USERPROFILE\.ssh\id_rsa

# Копируешь публичный ключ
type $env:USERPROFILE\.ssh\id_rsa.pub | clip
```

Этот ключ добавляешь при создании сервера в Hetzner.

#### Шаг 2.3: Подключаешься к серверу первый раз

```powershell
# Замени IP_СЕРВЕРА на реальный IP из консоли Hetzner
ssh root@IP_СЕРВЕРА

# Пример:
ssh root@138.201.123.456
```

При первом подключении может спросить - вводишь **yes**.

#### Шаг 2.4: Создаешь пользователя (опционально, но рекомендуется)

```bash
# На сервере:
adduser botuser
usermod -aG sudo botuser

# Переключаешься на нового пользователя
su - botuser
```

---

### **ЧАСТЬ 3: РАЗВЕРТЫВАНИЕ КОДА НА СЕРВЕР**

#### Вариант A: Через скрипт (АВТОМАТИЧЕСКИ)

```bash
# На сервере подключаешься как root
ssh root@IP_СЕРВЕРА

# Загружаешь и запускаешь скрипт setup.sh
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/telegram-bot-orders/main/setup.sh
chmod +x setup.sh

# Запускаешь скрипт с переменными
BOT_TOKEN="8283115795:AAHRJHjwXivexbPDH-HZg3ydCahBHlzROyM" \
ADMIN_CHAT_ID="-1003898978688" \
bash setup.sh
```

#### Вариант B: Вручную (ПОШАГОВО)

```bash
# 1. Подключаешься к серверу
ssh root@IP_СЕРВЕРА

# 2. Обновляешь пакеты
apt update && apt upgrade -y

# 3. Устанавливаешь Python и Git
apt install -y python3 python3-pip python3-venv git

# 4. Клонируешь репозиторий
cd /home
git clone https://github.com/YOUR_USERNAME/telegram-bot-orders.git telegram-bot
cd telegram-bot

# 5. Создаешь виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# 6. Устанавливаешь зависимости
pip install -r requirements.txt

# 7. Создаешь файл .env
cat > .env << 'EOF'
BOT_TOKEN=8283115795:AAHRJHjwXivexbPDH-HZg3ydCahBHlzROyM
ADMIN_CHAT_ID=-1003898978688
EOF

# 8. Делаешь .env недоступным для других
chmod 600 .env

# 9. Тестируешь бота вручную
python3 bot.py
# (Жми Ctrl+C чтобы остановить)

# 10. Создаешь systemd сервис для автозапуска
sudo tee /etc/systemd/system/telegram-bot.service > /dev/null << 'EOF'
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

# 11. Перезагружаешь systemd
sudo systemctl daemon-reload

# 12. Запускаешь бота
sudo systemctl start telegram-bot
sudo systemctl enable telegram-bot

# 13. Проверяешь статус
sudo systemctl status telegram-bot
```

---

### **ЧАСТЬ 4: ПРОВЕРКА И ЛОГИ**

#### Проверить, что бот работает:

```bash
# Посмотреть статус
systemctl status telegram-bot

# Посмотреть логи в реальном времени
journalctl -u telegram-bot -f

# Посмотреть последние 50 строк логов
journalctl -u telegram-bot -n 50
```

#### Если бот не запускается:

```bash
# Остановить бота
systemctl stop telegram-bot

# Запустить вручную для отладки
cd /home/telegram-bot
source venv/bin/activate
python3 bot.py

# Посмотреть ошибку в консоли
```

---

### **ЧАСТЬ 5: ОБНОВЛЕНИЯ КОДА**

После каждого обновления кода в GitHub бот автоматически обновляется:

```bash
# На сервере
cd /home/telegram-bot
git pull origin main

# Перезапускаешь бота
systemctl restart telegram-bot
```

Или создаешь GitHub Action для автоматического обновления (продвинутый вариант).

---

## ⚙️ GitHub Action для АВТОМАТИЧЕСКОГО развертывания (опционально)

Создаешь файл `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Hetzner

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Hetzner
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.SERVER_IP }}
        username: root
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /home/telegram-bot
          git pull origin main
          source venv/bin/activate
          pip install -r requirements.txt
          systemctl restart telegram-bot
```

---

## 🔐 Безопасность (ВАЖНО!)

1. **GitHub Secrets** - никогда не коммитим реальные токены
2. **.env в .gitignore** - файл не попадает на GitHub
3. **chmod 600 .env** - только владелец может читать
4. **Приватный репозиторий** - GitHub репо должен быть Private
5. **SSH ключ** - используй только для сервера, не шары его никому

---

## 📞 Если что-то не работает

### Бот не запускается?
```bash
systemctl status telegram-bot
journalctl -u telegram-bot -n 50
```

### Проблема с подключением к GitHub?
```bash
cd /home/telegram-bot
git remote -v
git fetch origin
```

### Проблема с токеном?
```bash
cat /home/telegram-bot/.env
# Проверь BOT_TOKEN и ADMIN_CHAT_ID
```

---

## 📊 Структура после развертывания

```
/home/telegram-bot/
├── bot.py
├── config.py
├── order_service.py
├── handlers.py
├── order_handlers.py
├── keyboards.py
├── states.py
├── utils.py
├── debug_tools.py
├── requirements.txt
├── .env                 (на сервере, НЕ в GitHub)
├── .gitignore
├── setup.sh
└── venv/               (виртуальное окружение)
```

---

## ✅ Готово!

После всех этих шагов:
- ✅ Код на GitHub
- ✅ Сервер Hetzner запущен
- ✅ Бот 24/7 работает на сервере
- ✅ Автоматически перезапускается при сбое
- ✅ Легко обновлять через `git push`

Вопросы? Спрашивай! 🚀
