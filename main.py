#!/usr/bin/env python3
import sys
import os

# ПРИНУДИТЕЛЬНЫЙ ВЫВОД ДЛЯ ОТЛАДКИ
print("[main.py] НАЧАЛО ЗАГРУЗКИ", flush=True)
print(f"[main.py] PYTHONPATH: {sys.path}", flush=True)
print(f"[main.py] Переменные окружения: TG_API_ID={os.environ.get('TG_API_ID')}, TG_API_HASH={os.environ.get('TG_API_HASH')}", flush=True)

# --- ОСТАЛЬНОЙ КОД НИЖЕ ---
import asyncio
import sys
from telethon import TelegramClient
from telethon.sessions import StringSession
import config
import collector
from analyzer import filter_important, summarize_only, verify_and_summarize
from reporter import send_report

print("[main.py] ВСЕ МОДУЛИ ЗАГРУЖЕНЫ", flush=True)

# ... (весь остальной код main.py, который у тебя уже есть)
