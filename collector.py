"""
Опрашивает каналы из channels.json, забирает сообщения новее последнего
обработанного (id хранится в state.json), возвращает список новых сообщений.
"""

import json
from datetime import datetime, timezone
from telethon import TelegramClient
import config


def load_channels() -> list[dict]:
    try:
        with open(config.CHANNELS_FILE, "r", encoding="utf-8") as f:
            channels = json.load(f)
            print(f"[collector] 📂 Загружено каналов: {len(channels)} из {config.CHANNELS_FILE}")
            return channels
    except FileNotFoundError:
        print(f"[collector] ⚠️  Файл {config.CHANNELS_FILE} не найден")
        return []


def load_sources() -> list[str]:
    try:
        with open(config.SOURCES_FILE, "r", encoding="utf-8") as f:
            sources = json.load(f)
            print(f"[collector] 📂 Загружено источников: {len(sources)} из {config.SOURCES_FILE}")
            return sources
    except FileNotFoundError:
        print(f"[collector] ⚠️  Файл {config.SOURCES_FILE} не найден")
        return []


def load_state() -> dict:
    try:
        with open(config.STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("[collector] 📂 Файл состояния не найден, начинаем с нуля")
        return {}


def save_state(state: dict):
    with open(config.STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("[collector] 💾 Состояние сохранено")


async def collect_new_messages(client: TelegramClient) -> list[dict]:
    channels = load_channels()
    state = load_state()
    all_new = []

    print(f"[collector] 🔍 Опрашиваю {len(channels)} каналов...")

    for i, ch in enumerate(channels, 1):
        username = ch["username"]
        last_id = state.get(username, 0)
        max_id_seen = last_id
        channel_new = []

        try:
            print(f"[collector]    [{i}/{len(channels)}] @{username} (последний ID: {last_id})")
            
            async for msg in client.iter_messages(username, limit=config.POLL_LIMIT_PER_CHANNEL):
                if msg.id <= last_id:
                    break
                if not msg.raw_text:
                    continue
                channel_new.append(msg)
                max_id_seen = max(max_id_seen, msg.id)
            
            print(f"[collector]       Найдено новых: {len(channel_new)}")
            
            for msg in channel_new:
                all_new.append({
                    "channel": username,
                    "text": msg.raw_text,
                    "date": msg.date.isoformat() if msg.date else datetime.now(timezone.utc).isoformat(),
                    "link": f"https://t.me/{username}/{msg.id}",
                    "verify": ch.get("verify", False),
                })
                
        except Exception as e:
            print(f"[collector]    ❌ Ошибка при опросе @{username}: {e}")
            continue

        state[username] = max_id_seen

    save_state(state)
    print(f"[collector] 📊 ИТОГО найдено новых сообщений: {len(all_new)}")
    
    if all_new:
        print(f"[collector] 📝 Первое новое сообщение из @{all_new[0]['channel']}")
    
    return all_new
