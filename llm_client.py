"""
Клиент для Qwen Code API (Alibaba Cloud DashScope)
OpenAI-совместимый API, 1000 запросов/день бесплатно
"""
import json
import requests
import os

# Конфигурация
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
QWEN_MODEL = os.environ.get("QWEN_MODEL", "qwen3-coder-plus")
QWEN_BASE_URL = os.environ.get("QWEN_BASE_URL", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1")

def generate(prompt: str, timeout: int = 120) -> str:
    """Отправляет промпт в Qwen Code API и возвращает ответ"""
    if not DASHSCOPE_API_KEY:
        raise ValueError("DASHSCOPE_API_KEY не задан!")
    
    # ПРОВЕРЬ: Убедись, что здесь стоит POST, а не GET!
    resp = requests.post(  # ← ДОЛЖЕН БЫТЬ POST!
        f"{QWEN_BASE_URL}/chat/completions",
        json={
            "model": QWEN_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        },
        timeout=timeout,
        headers={
            "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
            "Content-Type": "application/json"
        }
    )
    
    print(f"[llm_client] Статус ответа: {resp.status_code}")  # ← Добавь для отладки
    print(f"[llm_client] Ответ: {resp.text[:200]}")  # ← Добавь для отладки
    
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()

def generate_json(prompt: str, timeout: int = 120) -> dict:
    raw = generate(prompt, timeout=timeout)
    raw = raw.replace("```json", "").replace("```", "").strip()

    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1:
        raw = raw[start:end + 1]

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print(f"[llm_client] ⚠️ Не удалось распарсить JSON: {raw[:200]}")
        return {}
