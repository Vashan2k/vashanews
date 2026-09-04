import llm_client
import verifier

def filter_important(message_text: str) -> dict:
    prompt = f"""Ты — фильтр важности новостей. Тебе дан текст сообщения из Telegram-канала.
Определи, является ли это ВАЖНОЙ новостью (значимое событие, а не мем/реклама/бытовой пост).

Текст сообщения:
---
{message_text}
---

Ответь СТРОГО в формате JSON без пояснений вокруг, например:
{{"important": true, "reason": "краткое обоснование"}}"""

    result = llm_client.generate_json(prompt)
    if "important" not in result:
        return {"important": False, "reason": "не удалось разобрать ответ модели"}
    return result

def summarize_only(message_text: str, source_channel: str) -> dict:
    prompt = f"""Сократи эту новость из Telegram-канала "{source_channel}" до 2-3 предложений,
сохранив суть. Ответь СТРОГО в формате JSON:
{{"summary": "..."}}

Текст:
---
{message_text}
---"""
    result = llm_client.generate_json(prompt)
    summary = result.get("summary") or message_text[:300]
    return {
        "status": "unverified",
        "summary": summary,
        "confirmed_by": [],
        "note": "Проверка в источниках для этого канала отключена.",
    }

def verify_and_summarize(message_text: str, source_channel: str, domains: list[str]) -> dict:
    query = " ".join(message_text.split()[:12])
    search_results = verifier.search_all_sources(query, domains)

    evidence_lines = []
    for domain, results in search_results.items():
        if not results:
            evidence_lines.append(f"{domain}: ничего не найдено")
        else:
            for r in results:
                evidence_lines.append(f"{domain}: {r['title']} — {r['snippet'][:200]}")
    evidence_text = "\n".join(evidence_lines) if evidence_lines else "Результатов поиска нет."

    prompt = f"""Новость из Telegram-канала "{source_channel}":
---
{message_text}
---

Результаты поиска по источникам {', '.join(domains)}:
---
{evidence_text}
---

На основе результатов поиска определи, подтверждается ли новость.
Ответь СТРОГО в формате JSON:
{{
  "status": "confirmed" | "not_found" | "contradicted",
  "summary": "2-3 предложения с сутью новости",
  "confirmed_by": ["домены, где реально нашлось подтверждение"],
  "note": "если есть противоречия между источниками — опиши, иначе пустая строка"
}}"""

    result = llm_client.generate_json(prompt)
    if "status" not in result:
        return {
            "status": "not_found",
            "summary": message_text[:200],
            "confirmed_by": [],
            "note": "не удалось разобрать ответ модели при проверке",
        }
    return result