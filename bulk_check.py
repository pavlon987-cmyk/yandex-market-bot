import time
from bot.parser import YandexMarketBot
from utils.database import Database

def bulk_check_all():
    """Проверить все аккаунты"""
    db = Database()
    accounts = db.get_all_accounts(status='active')
    
    if not accounts:
        print("❌ Нет активных аккаунтов!")
        return
    
    print(f"🔍 Начинаю проверку {len(accounts)} аккаунтов...")
    print("="  50)
    
    bot = YandexMarketBot()
    
    try:
        bot.startbrowser(headless=True)
        
        results = {
            'success': 0,
            'failed': 0,
            'totalorders': 0,
            'hightrust': 0,
            'lowtrust': 0
        }
        
        for i, account in enumerate(accounts, 1):
            print(f"\n{i}/{len(accounts)} Проверка: {account'email'}")
            
            try:
                # Логин
                if not bot.login(account'email', account'password'):
                    print(f"  ❌ Ошибка входа")
                    results'failed' += 1
                    continue
                
                # Проверка траста
                trust = bot.checkaccounttrust(account'id')
                if trust:
                    print(f"  🎯 Траст: {trust'score'}/100")
                    
                    if trust'score' >= 80:
                        results'high_trust' += 1
                    elif trust'score' < 40:
                        results'low_trust'+= 1
                
                # Парсинг заказов
                orders = bot.parseorders(account['id'])
                if orders:
                    print(f"  📦 Заказов: {len(orders)}")
                    results['totalorders'] += len(orders)
                
                results'success' += 1
                print(f"  ✅ Успешно")
                
                # Задержка между аккаунтами
                time.sleep(3)except Exception as e:
                print(f"  ❌ Ошибка: {e}")
                results['failed'] += 1
                
                # Логируем ошибку
                db.add_log(
                    account_id=account['id'],
                    action='bulk_check_error',
                    details=str(e),
                    status='error'
                )
        
        # Итоговый отчёт
        print("\n" + "=" * 50)
        print("📊 ИТОГОВЫЙ ОТЧЁТ")
        print("=" * 50)
        print(f"✅ Успешно проверено: {results['success']}")
        print(f"❌ Ошибок: {results['failed']}")
        print(f"📦 Всего заказов: {results['total_orders']}")
        print(f"🟢 Высокий траст (80+): {results['high_trust']}")
        print(f"🔴 Низкий траст (<40): {results['low_trust']}")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        bot.close()
        print("\n✅ Проверка завершена!")

if __name__ == "__main__":
    bulk_check_all()