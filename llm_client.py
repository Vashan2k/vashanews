"""
Клиент для LLM7.io — бесплатный OpenAI-совместимый API
Без регистрации и карты
"""
import json
import os
from openai import OpenAI

# Конфигурация
LLM7_BASE_URL = "https://api.llm7.io/v1"
LLM7_API_KEY = os.environ.get("LLM7_API_KEY", "Lp4t2brwExYaz7ubDN/Xmj7HvOTMB8cJ8rwEGJX2DBcWTY1oKw/qwUxHiObIW+rkjumbDBTXfCjfgjtWDq1rd4awm7xPtyD9eeGF0tt2O1RUOwCoRvkmWbIiR/OcBCTbUtTUhiefvk/oqrwmrQ==") # реально работает, просто слово "unused"
LLM7_MODEL = "default"   # или "fast", "deepseek-r1", "qwen2.5" [citation:11][citation:12]

# Инициализируем клиент
client = OpenAI(
    api_key=LLM7_API_KEY,
    base_url=LLM7_BASE_URL,
)

def generate(prompt: str, timeout: int = 120) -> str:
    """Отправляет промпт в LLM7.io и возвращает ответ"""
    try:
        completion = client.chat.completions.create(
            model=LLM7_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            timeout=timeout
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"[llm_client] ❌ Ошибка: {e}")
        raise

def generate_json(prompt: str, timeout: int = 120) -> dict:
    """Просит модель вернуть JSON и парсит его"""
    raw = generate(prompt, timeout=timeout)
    raw = raw.replace("```json", "").replace("```", "").strip()

    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1:
        raw = raw[start:end + 1]

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print(f"[llm_client] ⚠️ Не удалось распарсить JSON")
        return {}
