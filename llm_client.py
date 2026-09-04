"""
Клиент для Qwen Code API (Alibaba Cloud DashScope)
Использует официальный OpenAI-совместимый SDK
"""
import json
import os
from openai import OpenAI

# Конфигурация
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
QWEN_MODEL = os.environ.get("QWEN_MODEL", "qwen-turbo")  # или qwen3.8-max-0902
QWEN_BASE_URL = os.environ.get("QWEN_BASE_URL", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1")

# Инициализируем клиент один раз
client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url=QWEN_BASE_URL,
)


def generate(prompt: str, timeout: int = 120) -> str:
    """Отправляет промпт в Qwen API и возвращает ответ"""
    if not DASHSCOPE_API_KEY:
        raise ValueError("DASHSCOPE_API_KEY не задан!")

    try:
        messages = [{"role": "user", "content": prompt}]
        
        completion = client.chat.completions.create(
            model=QWEN_MODEL,
            messages=messages,
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
        print(f"[llm_client] ⚠️ Не удалось распарсить JSON: {raw[:200]}...")
        return {}
