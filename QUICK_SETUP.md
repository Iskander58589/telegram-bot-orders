# ⚡ Быстрый чеклист развертывания (5 минут)

## 📋 Список дел

### ЛОКАЛЬНО (на твоем ПК)

- [ ] **Git инициализация**
  ```bash
  git init
  git add .
  git commit -m "Initial commit"
  git branch -M main
  git remote add origin https://github.com/YOUR_USERNAME/telegram-bot-orders.git
  git push -u origin main
  ```

- [ ] **GitHub репозиторий создан и приватный** ✅

- [ ] **GitHub Secrets добавлены**
  - [ ] BOT_TOKEN
  - [ ] ADMIN_CHAT_ID
  
  (Settings → Secrets and variables → Actions)

---

### HETZNER (сервер)

- [ ] **Аккаунт создан на hetzner.com** ✅

- [ ] **Сервер создан**
  - [ ] Ubuntu 22.04 LTS
  - [ ] SSH ключ добавлен
  - [ ] IP сервера скопирован

- [ ] **SSH подключение работает**
  ```bash
  ssh root@IP_СЕРВЕРА
  ```

---

### НА СЕРВЕРЕ

- [ ] **Скрипт развертывания запущен**
  ```bash
  BOT_TOKEN="твой_токен" ADMIN_CHAT_ID="твой_id" bash setup.sh
  ```

  ИЛИ развертывание вручную:
  
- [ ] **Git клонирован**
  ```bash
  git clone https://github.com/YOUR_USERNAME/telegram-bot-orders.git /home/telegram-bot
  ```

- [ ] **Виртуальное окружение создано**
  ```bash
  cd /home/telegram-bot
  python3 -m venv venv
  source venv/bin/activate
  ```

- [ ] **Зависимости установлены**
  ```bash
  pip install -r requirements.txt
  ```

- [ ] **.env файл создан**
  ```bash
  cat > .env << EOF
  BOT_TOKEN=твой_токен
  ADMIN_CHAT_ID=твой_id
  EOF
  chmod 600 .env
  ```

- [ ] **Бот тестирован вручную**
  ```bash
  python3 bot.py
  # Жми Ctrl+C
  ```

- [ ] **systemd сервис создан и запущен**
  ```bash
  systemctl start telegram-bot
  systemctl enable telegram-bot
  systemctl status telegram-bot
  ```

---

## 🔍 Проверка

### Бот работает?
```bash
systemctl status telegram-bot
```

Должно быть: `active (running)`

### Тест в Telegram
Напиши боту `/start` - если ответит, все работает! ✅

---

## 🚨 Если что-то не работает

1. **Ошибка подключения к GitHub?**
   ```bash
   cd /home/telegram-bot
   git status
   ```

2. **Бот не запускается?**
   ```bash
   journalctl -u telegram-bot -n 50
   ```

3. **Проблема с переменными окружения?**
   ```bash
   cat /home/telegram-bot/.env
   echo $BOT_TOKEN
   echo $ADMIN_CHAT_ID
   ```

4. **Python не найден?**
   ```bash
   which python3
   apt install -y python3 python3-pip python3-venv
   ```

---

## 📞 Поддержка

Полная документация: `HETZNER_DEPLOYMENT.md`
