from dotenv import load_dotenv
load_dotenv()

import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import refund
from database.db import Database
from keyboards.main_kb import get_main_keyboard

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(storage=MemoryStorage())
db = Database()

# Регистрация роутера
dp.include_router(refund.router)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await db.add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )
    
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "🤖 Я помогу тебе вернуть деньги за заказ с Яндекс.Маркет\n\n"
        "🎯 **ЧТО Я УМЕЮ:**\n"
        "✅ Анализирую политику возврата в реальном времени\n"
        "✅ Нахожу законные основания для возврата\n"
        "✅ Генерирую готовые претензии с AI\n"
        "✅ Подсказываю лазейки БЕЗ возврата товара\n\n"
        "Выбери действие:",
        reply_markup=get_main_keyboard()
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "📚 **КАК ПОЛЬЗОВАТЬСЯ:**\n\n"
        "1️⃣ Нажми '🔄 Новый возврат'\n"
        "2️⃣ Введи номер заказа\n"
        "3️⃣ Опиши проблему\n"
        "4️⃣ Получи готовую претензию с AI-анализом\n"
        "5️⃣ Отправь в поддержку Яндекса\n\n"
        "💡 **ВАЖНО:**\n"
        "- Закон на твоей стороне (ЗоЗПП)\n"
        "- AI найдёт законные основания\n"
        "- Часто можно НЕ возвращать товар!",
        reply_markup=get_main_keyboard()
    )

async def main():
    logger.info("🚀 Бот запущен!")
    await db.create_tables()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
