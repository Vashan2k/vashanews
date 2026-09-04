import json
from datetime import datetime, timezone
from telethon import TelegramClient
import config

def load_channels() -> list[dict]:
    try:
        with open(config.CHANNELS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def load_sources() -> list[str]:
    try:
        with open(config.SOURCES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def load_state() -> dict:
    try:
        with open(config.STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_state(state: dict):
    with open(config.STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

async def collect_new_messages(client: TelegramClient) -> list[dict]:
    channels = load_channels()
    state = load_state()
    all_new = []

    for ch in channels:
        username = ch["username"]
        last_id = state.get(username, 0)
        max_id_seen = last_id

        try:
            async for msg in client.iter_messages(username, limit=config.POLL_LIMIT_PER_CHANNEL):
                if msg.id <= last_id:
                    break
                if not msg.raw_text:
                    continue
                all_new.append({
                    "channel": username,
                    "text": msg.raw_text,
                    "date": msg.date.isoformat() if msg.date else datetime.now(timezone.utc).isoformat(),
                    "link": f"https://t.me/{username}/{msg.id}",
                    "verify": ch.get("verify", False),
                })
                max_id_seen = max(max_id_seen, msg.id)
        except Exception as e:
            print(f"[collector] Ошибка при опросе @{username}: {e}")
            continue

        state[username] = max_id_seen

    save_state(state)
    print(f"[collector] Найдено новых сообщений: {len(all_new)}")
    return all_new