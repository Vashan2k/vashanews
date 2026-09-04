from ddgs import DDGS

def search_domain(query: str, domain: str, max_results: int = 3) -> list[dict]:
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(f"{query} site:{domain}", max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", ""),
                })
    except Exception as e:
        print(f"[verifier] Ошибка поиска на {domain}: {e}")
    return results

def search_all_sources(query: str, domains: list[str], max_results_per_domain: int = 3) -> dict:
    return {domain: search_domain(query, domain, max_results_per_domain) for domain in domains}