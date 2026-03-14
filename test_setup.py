
# test_setup.py
from bot.config import settings
from openai import OpenAI

print("🔍 Проверяем настройки...")
print(f"✅ Telegram токен: {settings.telegram_bot_token[:20]}...")
print(f"✅ Admin ID: {settings.admin_id}")
print(f"✅ LLM провайдер: {settings.llm_provider}")
print(f"✅ LLM ключ: {settings.llm_api_key[:20]}...")

print("\n🤖 Тестируем Groq API...")

client = OpenAI(
    api_key=settings.llm_api_key,
    base_url=settings.llm_base_url
)

try:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": "Скажи 'Работаю!' на русском"}
        ],
        max_tokens=50
    )
    
    print(f"✅ ОТВЕТ ОТ GROQ: {response.choices[0].message.content}")
    print("\n🎉 ВСЁ РАБОТАЕТ! МОЖНО ПРОДОЛЖАТЬ!")
    
except Exception as e:
    print(f"❌ ОШИБКА: {e}")
