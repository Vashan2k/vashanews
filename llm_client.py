"""
Клиент для FreeLLM — бесплатный агрегатор LLM
Не требует API-ключей и работает с 15+ провайдерами
"""
import json
import requests
import ssl

# Отключаем предупреждения SSL
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FREELLM_URL = "https://api.freellm.xyz/v1"
DEFAULT_MODEL = "mistral"

def generate(prompt: str, timeout: int = 120) -> str:
    """Отправляет промпт в FreeLLM и возвращает ответ"""
    try:
        resp = requests.post(
            f"{FREELLM_URL}/chat/completions",
            json={
                "model": DEFAULT_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            },
            timeout=timeout,
            headers={"Content-Type": "application/json"},
            verify=False  # ← ОТКЛЮЧАЕМ ПРОВЕРКУ SSL
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.exceptions.ConnectionError:
        print("[llm_client] ❌ Не удалось подключиться к FreeLLM. Проверь интернет.")
        raise
    except requests.exceptions.Timeout:
        print("[llm_client] ⏰ Таймаут запроса к FreeLLM")
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
        print(f"[llm_client] ⚠️ Не удалось распарсить JSON: {raw[:200]}...")
        return {}
