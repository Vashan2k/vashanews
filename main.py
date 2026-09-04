# В начале main() после импортов:

async def main():
    print("[main] 🚀 Telegram News Agent запускается...")
    
    # Проверяем FreeLLM
    try:
        test = llm_client.generate("Say hello")
        print("[main] ✅ FreeLLM работает!")
    except Exception as e:
        print(f"[main] ❌ FreeLLM не отвечает: {e}")
        print("[main] ⚠️ Проверь интернет или попробуй другую модель")
    
    # ... остальной код
