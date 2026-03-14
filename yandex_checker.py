from playwright.async_api import async_playwright
import asyncio
from openai import AsyncOpenAI
from config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def check_yandex_order(order_number: str, phone: str) -> dict:
    """Проверяет заказ в Яндекс.Маркет и анализирует с помощью AI"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # Переходим на страницу заказов Яндекс.Маркет
            await page.goto('https://market.yandex.ru/my/orders', timeout=30000)
            
            # Ждём загрузки страницы
            await page.wait_for_timeout(3000)
            
            # Получаем скриншот для AI анализа
            screenshot = await page.screenshot(full_page=True)
            
            # Получаем текст страницы
            page_text = await page.content()
            
            await browser.close()
            
            # Анализируем с помощью GPT-4
            analysis = await analyze_with_gpt(order_number, phone, page_text[:4000])
            
            return {
                'success': True,
                'order_found': 'заказ' in page_text.lower() or order_number in page_text,
                'analysis': analysis
            }
            
        except Exception as e:
            await browser.close()
            return {
                'success': False,
                'error': str(e),
                'analysis': 'Не удалось проверить заказ'
            }

async def analyze_with_gpt(order_number: str, phone: str, page_content: str) -> str:
    """Анализирует информацию о заказе с помощью GPT-4"""
    
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """Ты помощник по возврату товаров из Яндекс.Маркет. 
                    Анализируй информацию о заказе и давай рекомендации:
                    - Можно ли вернуть товар?
                    - Какие шаги предпринять?
                    - Какие документы нужны?
                    Отвечай кратко и по делу на русском языке."""
                },
                {
                    "role": "user",
                    "content": f"""
                    Номер заказа: {order_number}
                    Телефон: {phone}
                    
                    Информация со страницы:
                    {page_content[:2000]}
                    
                    Дай рекомендации по возврату этого заказа.
                    """
                }
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"⚠️ Ошибка AI анализа: {str(e)}"
