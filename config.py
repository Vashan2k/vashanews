"""
Конфигурация для Render.com
"""
import os

TG_API_ID = int(os.environ.get("TG_API_ID", "0"))
TG_API_HASH = os.environ.get("TG_API_HASH", "")
TG_SESSION_NAME = "news_agent_session"
TG_SESSION_STRING = os.environ.get("TG_SESSION_STRING", "")

TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
TG_REPORT_CHAT_ID = os.environ.get("TG_REPORT_CHAT_ID", "")

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.environ.get("OPENROUTER_MODEL", "meta-llama/llama-3.2-3b-instruct:free")

CHANNELS_FILE = "channels.json"
STATE_FILE = "state.json"
SOURCES_FILE = "sources.json"

POLL_LIMIT_PER_CHANNEL = 30
REPORT_INTERVAL_MINUTES = 60