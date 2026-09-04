"""
Конфигурация для Render.com
"""
import os
import logging

# --- Настройка логирования ---
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# --- Telegram User API ---
TG_API_ID = int(os.environ.get("TG_API_ID", "0"))
TG_API_HASH = os.environ.get("TG_API_HASH", "")
TG_SESSION_NAME = "news_agent_session"
TG_SESSION_STRING = os.environ.get("TG_SESSION_STRING", "")

# --- Telegram Bot API ---
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
TG_REPORT_CHAT_ID = os.environ.get("TG_REPORT_CHAT_ID", "")

# --- OpenRouter ---
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = "openrouter/free"

# --- Файлы ---
CHANNELS_FILE = "channels.json"
STATE_FILE = "state.json"
SOURCES_FILE = "sources.json"

# --- Параметры ---
POLL_LIMIT_PER_CHANNEL = 30
REPORT_INTERVAL_MINUTES = 0.1
