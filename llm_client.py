"""
Клиент для Qwen Code API (Alibaba Cloud DashScope)
OpenAI-совместимый API, 1000 запросов/день бесплатно
"""
import json
import requests
import os

# Конфигурация
QWEN_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
QWEN_MODEL = os.environ.get("QWEN_MODEL", "qwen3-coder-plus")
QWEN_BASE_URL = os.environ.get("QWEN_BASE_URL", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1")

def generate(prompt: str, timeout: int = 120) -> str:
    """Отправляет промпт в Qwen Code API и возвращает ответ"""
    if not QWEN_API_KEY:
        raise ValueError("DASHSCOPE_API_KEY не задан! Получи ключ на qwencloud.com")
    
    try:
        resp = requests.post(
            f"{QWEN_BASE_URL}/chat/completions",
            json={
                "model": QWEN_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            },
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {QWEN_API_KEY}",
                "Content-Type": "application/json"
            }
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.exceptions.ConnectionError:
        print("[llm_client] ❌ Не удалось подключиться к Qwen API")
        raise
    except requests.exceptions.Timeout:
        print("[llm_client] ⏰ Таймаут запроса к Qwen API")
        raise
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
        
