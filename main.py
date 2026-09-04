import asyncio
import sys
from telethon import TelegramClient
from telethon.sessions import StringSession
import config
import collector
from analyzer import filter_important, summarize_only, verify_and_summarize
from reporter import send_report

async def run_once(client: TelegramClient):
    messages = await collector.collect_new_messages(client)
    if not messages:
        print("[main] Новых сообщений нет.")
        return

    sources = collector.load_sources()
    report_items = []

    for msg in messages:
        try:
            importance = filter_important(msg["text"])
        except Exception as e:
            print(f"[main] Ошибка фильтрации ({msg['channel']}): {e}")
            continue

        if not importance.get("important"):
            continue

        print(f"[main] Важная новость из @{msg['channel']}")

        try:
            if msg.get("verify") and sources:
                result = verify_and_summarize(msg["text"], msg["channel"], sources)
            else:
                result = summarize_only(msg["text"], msg["channel"])
        except Exception as e:
            print(f"[main] Ошибка обработки ({msg['channel']}): {e}")
            continue

        report_items.append(result)

    await send_report(report_items)

async def main():
    if config.TG_SESSION_STRING:
        session = StringSession(config.TG_SESSION_STRING)
    else:
        session = config.TG_SESSION_NAME

    client = TelegramClient(session, config.TG_API_ID, config.TG_API_HASH)
    async with client:
        if "--loop" in sys.argv:
            interval = config.REPORT_INTERVAL_MINUTES * 60
            print(f"[main] Демон, интервал {config.REPORT_INTERVAL_MINUTES} мин.")
            while True:
                await run_once(client)
                await asyncio.sleep(interval)
        else:
            await run_once(client)

if __name__ == "__main__":
    asyncio.run(main())