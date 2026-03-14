
import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import start, refund, questions

async def main():
    """Главная функция запуска бота"""
    
    # Инициализация бота
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    # Регистрируем все роутеры
    dp.include_router(start.router)
    dp.include_router(refund.router)
    dp.include_router(questions.router)
    
    # Удаляем старые вебхуки (чтобы избежать конфликтов)
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Выводим статус запуска
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("✅ Бот запущен с анализатором 2026!")
    print("🔍 Проверка политик в реальном времени активна!")
    print("📊 Доступно 15+ проверенных багов")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Запускаем polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Настраиваем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Запускаем бота
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n❌ Бот остановлен пользователем")
    except Exception as e:
        print(f"\n🔴 ОШИБКА: {e}")
