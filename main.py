print("[main.py] ВСЕ МОДУЛИ ЗАГРУЖЕНЫ", flush=True)

# --- ТЕПЕРЬ ЛОГИРУЕМ КАЖДЫЙ ШАГ ---
print("[main.py] ШАГ 1: Начинаю асинхронный main()", flush=True)

async def main():
    print("[main] 🚀 Telegram News Agent запускается...", flush=True)
    
    print(f"[main] 🔑 Использую сессию: {'строковая' if config.TG_SESSION_STRING else 'файловая'}", flush=True)
    
    if config.TG_SESSION_STRING:
        session = StringSession(config.TG_SESSION_STRING)
    else:
        session = config.TG_SESSION_NAME

    print("[main] 📡 Подключаюсь к Telegram API...", flush=True)
    client = TelegramClient(session, config.TG_API_ID, config.TG_API_HASH)
    
    try:
        await client.start()
        print("[main] ✅ Подключение к Telegram установлено!", flush=True)
        me = await client.get_me()
        print(f"[main] 👤 Аккаунт: @{me.username}", flush=True)
    except Exception as e:
        print(f"[main] ❌ Ошибка подключения к Telegram: {e}", flush=True)
        return
    
    async with client:
        if "--loop" in sys.argv:
            interval = config.REPORT_INTERVAL_MINUTES * 60
            print(f"[main] 🔄 Работаю в режиме ДЕМОНА, интервал {config.REPORT_INTERVAL_MINUTES} мин.", flush=True)
            
            while True:
                try:
                    await run_once(client)
                except Exception as e:
                    print(f"[main] ❌ Критическая ошибка в цикле: {e}", flush=True)
                print(f"[main] 💤 Следующая проверка через {config.REPORT_INTERVAL_MINUTES} минут...", flush=True)
                await asyncio.sleep(interval)
        else:
            print("[main] 🔄 Работаю в РАЗОВОМ режиме", flush=True)
            await run_once(client)
            print("[main] ✅ Разовый запуск завершён", flush=True)

if __name__ == "__main__":
    print("[main.py] ШАГ 2: Запускаю asyncio.run(main())", flush=True)
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"[main.py] ❌ КРИТИЧЕСКАЯ ОШИБКА: {e}", flush=True)
        import traceback
        traceback.print_exc()
