"""
Утилита для управления списком мониторимых каналов.
Использование:
    python manage_channels.py list
    python manage_channels.py add <username> [--verify]
    python manage_channels.py remove <username>
    python manage_channels.py toggle <username>
    python manage_channels.py sources
    python manage_channels.py add-source <domain>
    python manage_channels.py remove-source <domain>
"""

import json
import sys
import config

def load_channels() -> list[dict]:
    try:
        with open(config.CHANNELS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_channels(channels: list[dict]):
    with open(config.CHANNELS_FILE, "w", encoding="utf-8") as f:
        json.dump(channels, f, ensure_ascii=False, indent=2)

def load_sources() -> list[str]:
    try:
        with open(config.SOURCES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_sources(sources: list[str]):
    with open(config.SOURCES_FILE, "w", encoding="utf-8") as f:
        json.dump(sources, f, ensure_ascii=False, indent=2)

def cmd_list():
    channels = load_channels()
    if not channels:
        print("Список каналов пуст.")
        return
    print(f"{'Канал':<30} {'Проверка в источниках'}")
    print("-" * 55)
    for ch in channels:
        flag = "✅ да" if ch.get("verify") else "—  нет"
        print(f"@{ch['username']:<29} {flag}")

def cmd_add(username: str, verify: bool):
    channels = load_channels()
    username = username.lstrip("@")
    if any(ch["username"] == username for ch in channels):
        print(f"Канал @{username} уже есть в списке.")
        return
    channels.append({"username": username, "verify": verify})
    save_channels(channels)
    print(f"Добавлен @{username} (проверка: {'да' if verify else 'нет'}).")

def cmd_remove(username: str):
    channels = load_channels()
    username = username.lstrip("@")
    new_channels = [ch for ch in channels if ch["username"] != username]
    if len(new_channels) == len(channels):
        print(f"Канал @{username} не найден.")
        return
    save_channels(new_channels)
    print(f"Канал @{username} удалён.")

def cmd_toggle(username: str):
    channels = load_channels()
    username = username.lstrip("@")
    for ch in channels:
        if ch["username"] == username:
            ch["verify"] = not ch.get("verify", False)
            save_channels(channels)
            print(f"Проверка для @{username} теперь: {'да' if ch['verify'] else 'нет'}.")
            return
    print(f"Канал @{username} не найден.")

def cmd_sources():
    sources = load_sources()
    if not sources:
        print("Список источников пуст.")
        return
    for s in sources:
        print(f"- {s}")

def cmd_add_source(domain: str):
    sources = load_sources()
    if domain in sources:
        print(f"{domain} уже есть в списке источников.")
        return
    sources.append(domain)
    save_sources(sources)
    print(f"Добавлен источник: {domain}")

def cmd_remove_source(domain: str):
    sources = load_sources()
    new_sources = [s for s in sources if s != domain]
    if len(new_sources) == len(sources):
        print(f"{domain} не найден в списке источников.")
        return
    save_sources(new_sources)
    print(f"Источник {domain} удалён.")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "list":
        cmd_list()
    elif cmd == "add" and len(sys.argv) >= 3:
        verify = "--verify" in sys.argv
        cmd_add(sys.argv[2], verify)
    elif cmd == "remove" and len(sys.argv) >= 3:
        cmd_remove(sys.argv[2])
    elif cmd == "toggle" and len(sys.argv) >= 3:
        cmd_toggle(sys.argv[2])
    elif cmd == "sources":
        cmd_sources()
    elif cmd == "add-source" and len(sys.argv) >= 3:
        cmd_add_source(sys.argv[2])
    elif cmd == "remove-source" and len(sys.argv) >= 3:
        cmd_remove_source(sys.argv[2])
    else:
        print(__doc__)

if __name__ == "__main__":
    main()