"""
Запустите этот скрипт ОДИН РАЗ на своём компьютере.
Он попросит номер телефона и код из Telegram, и выведет строку сессии.

Запуск:
    export TG_API_ID=...
    export TG_API_HASH=...
    python generate_session.py
"""

import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = int(os.environ["TG_API_ID"])
api_hash = os.environ["TG_API_HASH"]

with TelegramClient(StringSession(), api_id, api_hash) as client:
    session_string = client.session.save()
    print("\n" + "=" * 60)
    print("Готово! Ваша строка сессии (сохраните как секрет TG_SESSION_STRING):")
    print("=" * 60)
    print(session_string)
    print("=" * 60)
    print("\nНЕ публикуйте эту строку нигде и не отправляйте её никому.")