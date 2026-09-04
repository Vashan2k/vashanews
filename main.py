#!/usr/bin/env python3
import sys
import os
import asyncio  # ← ВАЖНО! Добавил

# ПРИНУДИТЕЛЬНЫЙ ВЫВОД ДЛЯ ОТЛАДКИ
print("[main.py] НАЧАЛО ЗАГРУЗКИ", flush=True)
print(f"[main.py] PYTHONPATH: {sys.path}", flush=True)
print(f"[main.py] Переменные окружения: TG_API_ID={os.environ.get('TG_API_ID')}, TG_API_HASH={os.environ.get('TG_API_HASH')}", flush=True)

# --- ИМПОРТЫ ---
from telethon import TelegramClient
from telethon.sessions import StringSession
import config
import collector
from analyzer import filter_important, summarize_only, verify_and_summarize
from reporter import send_report

print("[main.py] ВСЕ МОДУЛИ ЗАГРУЖЕНЫ", flush=True)

# --- ФУНКЦИИ ---
async def run_once(client: TelegramClient):
    print(f"[main] 🚀 Начинаю проверку...", flush=True)
    
    messages = await collector.collect_new_messages(client)
    if not messages:
        print("[main] ❌ Новых сообщений нет.", flush=True)
        return

    sources = collector.load_sources()
    report_items = []

    for msg in messages:
        try:
            importance = filter_important(msg["text"])
        except Exception as e:
            print(f"[main] ❌ Ошибка фильтрации (@{msg['channel']}): {e}", flush=True)
            continue

        if not importance.get("important"):
            continue

        print(f"[main] ✅ Важная новость из @{msg['channel']}", flush=True)

        try:
            if msg.get("verify") and sources:
                result = verify_and_summarize(msg["text"], msg["channel"], sources)
            else:
                result = summarize_only(msg["text"], msg["channel"])
        except Exception as e:
            print(f"[main] ❌ Ошибка обработки (@{msg['channel']}): {e}", flush=True)
            continue

        report_items.append(result)

    await send_report(report_items)
    print(f"[main] ✅ Цикл завершён", flush=True)

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
    print("[main.py] Шаг 2: Запускаю asyncio.run(main())", flush=True)
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"[main.py] ❌ КРИТИЧЕСКАЯ ОШИБКА: {e}", flush=True)
        import traceback
        traceback.print_exc()
