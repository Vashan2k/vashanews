# Telegram News Agent — бесплатный хостинг на Render.com

Агент мониторит Telegram-каналы, фильтрует важные новости через OpenRouter (бесплатно) и отправляет дайджест в Telegram.

## 🚀 Деплой на Render.com

### 1. Зарегистрироваться
- https://render.com (бесплатно, карта не нужна)
- https://openrouter.ai (бесплатно, карта не нужна)

### 2. Получить ключи
- **Telegram API**: https://my.telegram.org → API development tools
- **Telegram Bot**: @BotFather → создать бота
- **Chat ID**: @userinfobot → узнать свой ID
- **OpenRouter Key**: https://openrouter.ai → Dashboard → API Keys

### 3. Сгенерировать сессию Telethon
```bash
pip install telethon
export TG_API_ID=ваш_api_id
export TG_API_HASH=ваш_api_hash
python generate_session.py