"""
Главный файл запуска бота для приёма заказов на учебные работы
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from config import BOT_TOKEN
from handlers import router as handlers_router
from order_handlers import router as order_handlers_router


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def setup_bot_commands(bot: Bot) -> None:
    """
    Установка команд бота в меню
    """
    commands = [
        BotCommand(command="start", description="Начать работу с ботом"),
        BotCommand(command="help", description="Помощь"),
    ]
    await bot.set_my_commands(commands)


async def main():
    """
    Главная функция запуска бота
    """
    # Инициализируем хранилище для FSM
    storage = MemoryStorage()
    
    # Создаём бота и диспетчер
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=storage)
    
    # Подключаем обработчики
    dp.include_router(handlers_router)
    dp.include_router(order_handlers_router)
    
    # Устанавливаем команды
    await setup_bot_commands(bot)
    
    try:
        logger.info("🚀 Бот запущен!")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())