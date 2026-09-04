"""
Точка входа. Делает ОДИН проход:
  собрать новые сообщения -> отфильтровать важные -> проверить -> отправить отчёт
"""

import asyncio
import sys
from datetime import datetime
from telethon import TelegramClient
from telethon.sessions import StringSession
import config
import collector
from analyzer import filter_important, summarize_only, verify_and_summarize
from reporter import send_report


async def run_once(client: TelegramClient):
    print(f"[main] 🚀 Начинаю проверку в {datetime.now().strftime('%H:%M:%S')}")
    
    # Загружаем список каналов
    channels = collector.load_channels()
    print(f"[main] 📋 Загружено каналов: {len(channels)}")
    for ch in channels:
        print(f"[main]    - @{ch['username']} (verify: {ch.get('verify', False)})")
    
    messages = await collector.collect_new_messages(client)
    
    if not messages:
        print("[main] ❌ Новых сообщений нет.")
        print("[main] 💤 Жду следующего цикла...")
        return
    
    print(f"[main] ✅ Найдено новых сообщений: {len(messages)}")

    sources = collector.load_sources()
    print(f"[main] 📰 Загружено источников для проверки: {len(sources)}")
    report_items = []

    for i, msg in enumerate(messages, 1):
        print(f"[main] 🔍 Обрабатываю сообщение {i}/{len(messages)} из @{msg['channel']}")
        print(f"[main]    Текст: {msg['text'][:100]}...")
        
        try:
            importance = filter_important(msg["text"])
        except Exception as e:
            print(f"[main] ❌ Ошибка фильтрации (@{msg['channel']}): {e}")
            continue

        if not importance.get("important"):
            print(f"[main] ⏭️  Сообщение из @{msg['channel']} признано НЕважным")
            continue

        print(f"[main] ✅ Сообщение из @{msg['channel']} ВАЖНОЕ!")
        print(f"[main]    Причина: {importance.get('reason', 'не указана')}")

        try:
            if msg.get("verify") and sources:
                print(f"[main] 🔎 Проверяю по источникам: {', '.join(sources)}")
                result = verify_and_summarize(msg["text"], msg["channel"], sources)
            else:
                print(f"[main] 📝 Делаю краткую сводку (без проверки)")
                result = summarize_only(msg["text"], msg["channel"])
        except Exception as e:
            print(f"[main] ❌ Ошибка обработки (@{msg['channel']}): {e}")
            continue

        report_items.append(result)
        print(f"[main] ✅ Добавлен отчёт для @{msg['channel']}")

    print(f"[main] 📊 Всего важных новостей: {len(report_items)}")
    await send_report(report_items)
    print(f"[main] ✅ Цикл завершён в {datetime.now().strftime('%H:%M:%S')}")


async def main():
    print("[main] 🚀 Telegram News Agent запускается...")
    
    if config.TG_SESSION_STRING:
        session = StringSession(config.TG_SESSION_STRING)
        print("[main] 🔑 Использую строковую сессию")
    else:
        session = config.TG_SESSION_NAME
        print("[main] 📁 Использую файловую сессию")

    client = TelegramClient(session, config.TG_API_ID, config.TG_API_HASH)
    
    print(f"[main] 📡 Подключаюсь к Telegram API...")
    await client.start()
    print("[main] ✅ Подключение к Telegram установлено")
    
    async with client:
        if "--loop" in sys.argv:
            interval = config.REPORT_INTERVAL_MINUTES * 60
            print(f"[main] 🔄 Работаю в режиме ДЕМОНА")
            print(f"[main] ⏱️  Интервал: {config.REPORT_INTERVAL_MINUTES} минут")
            print(f"[main] 🎯 Каналы: {', '.join([ch['username'] for ch in collector.load_channels()])}")
            print("[main] 🟢 Бот запущен и ждёт сообщений...")
            
            while True:
                try:
                    await run_once(client)
                except Exception as e:
                    print(f"[main] ❌ Критическая ошибка в цикле: {e}")
                print(f"[main] 💤 Следующая проверка через {config.REPORT_INTERVAL_MINUTES} минут...")
                await asyncio.sleep(interval)
        else:
            print("[main] 🔄 Работаю в РАЗОВОМ режиме")
            await run_once(client)
            print("[main] ✅ Разовый запуск завершён")


if __name__ == "__main__":
    print("[main] 🟢 Запуск main.py...")
    asyncio.run(main())
