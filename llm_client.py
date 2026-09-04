"""
Клиент для KeylessAI — бесплатный OpenAI-совместимый прокси.
Не требует API-ключей и регистрации.
"""
import json
import requests

# Публичный эндпоинт KeylessAI
KEYLESSAI_URL = "https://keylessai.thryx.workers.dev/v1"

def generate(prompt: str, timeout: int = 120) -> str:
    """Отправляет промпт через KeylessAI и возвращает ответ."""
    try:
        resp = requests.post(
            f"{KEYLESSAI_URL}/chat/completions",
            json={
                "model": "gpt-4o",  # Будет автоматически заменён на бесплатный аналог[citation:9]
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            },
            timeout=timeout,
            headers={
                "Content-Type": "application/json"
                # API-ключ не нужен, можно передать любую строку или оставить пустым[citation:9]
            }
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.exceptions.ConnectionError:
        print("[llm_client] ❌ Не удалось подключиться к KeylessAI. Проверь интернет.")
        raise
    except requests.exceptions.Timeout:
        print("[llm_client] ⏰ Таймаут запроса к KeylessAI")
        raise
    except Exception as e:
        print(f"[llm_client] ❌ Ошибка: {e}")
        raise

def generate_json(prompt: str, timeout: int = 120) -> dict:
    """Просит модель вернуть JSON и парсит его."""
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
