"""
Конфигурация для Render.com
"""
import os

# --- Telegram User API ---
TG_API_ID = int(os.environ.get("TG_API_ID", "0"))
TG_API_HASH = os.environ.get("TG_API_HASH", "")
TG_SESSION_NAME = "news_agent_session"
TG_SESSION_STRING = os.environ.get("TG_SESSION_STRING", "")

# --- Telegram Bot API ---
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
TG_REPORT_CHAT_ID = os.environ.get("TG_REPORT_CHAT_ID", "")

# --- Qwen Code API (DashScope) ---
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
QWEN_MODEL = os.environ.get("QWEN_MODEL", "qwen-turbo")  # бесплатная модель
QWEN_BASE_URL = os.environ.get("QWEN_BASE_URL", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1")

# --- Файлы ---
CHANNELS_FILE = "channels.json"
STATE_FILE = "state.json"
SOURCES_FILE = "sources.json"

# --- Параметры ---
POLL_LIMIT_PER_CHANNEL = 30
REPORT_INTERVAL_MINUTES = 30
