import sys
from bot.parser import YandexMarketBot
from utils.database import Database

def testsingleaccount():
    """Тест одного аккаунта"""
    db = Database()
    
    # Получаем первый аккаунт
    accounts = db.getallaccounts(limit=1)
    
    if not accounts:
        print("❌ Нет аккаунтов в базе!")
        print("Добавьте аккаунт через Telegram бота")
        return
    
    account = accounts[0]
    
    print(f"🔍 Тестирую аккаунт: {account['email']}")
    print("=" * 50)
    
    # Создаём бота
    bot = YandexMarketBot()
    
    try:
        # Запускаем браузер
        print("🌐 Запуск браузера...")
        bot.startbrowser(headless=False)  # Видимый режим для теста
        
        # Логин
        print(f"🔐 Вход в аккаунт {account'email'}...")
        if not bot.login(account'email', account'password'):
            print("❌ Ошибка входа!")
            return
        
        print("✅ Успешный вход!")
        
        # Проверка траста
        print("\n🎯 Проверка траста...")
        trustresult = bot.checkaccounttrust(account['id'])
        
        if trustresult:
            print(f"✅ Траст проверен: {trustresult['score']}/100")
            print(f"📊 Уровень: {trustresult'level'}")
            print("\nДетали:")
            for detail in trustresult['details']:
                print(f"  • {detail}")
        
        # Парсинг заказов
        print("\n📦 Парсинг заказов...")
        orders = bot.parseorders(account'id')
        
        if orders:
            print(f"✅ Спарсено заказов: {len(orders)}")
            print("\nПоследние 3 заказа:")
            for order in orders:3:
                print(f"\n  📦 {order'number'}")
                print(f"     {order'product':50}...")
                print(f"     💰 {order'price'} | 📅 {order'date'}")
                print(f"     📊 {order'status'}")
        
        print("\n" + "="  50)
        print("✅ Тест завершён успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n🔒 Закрытие браузера...")
        bot.close()

if __name__ == "__main__":
    test_single_account()