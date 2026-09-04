from telegram import Bot
from telegram.constants import ParseMode
import config

bot = Bot(token=config.TG_BOT_TOKEN)

STATUS_EMOJI = {
    "confirmed": "✅",
    "not_found": "❓",
    "contradicted": "⚠️",
    "unverified": "ℹ️",
}

def build_report_text(items: list[dict]) -> str:
    if not items:
        return "За этот период важных новостей не найдено."

    lines = ["📰 *Сводка важных новостей*\n"]

    for item in items:
        emoji = STATUS_EMOJI.get(item.get("status"), "❓")
        lines.append(f"{emoji} {item.get('summary', '')}")
        confirmed_by = item.get("confirmed_by") or []
        if confirmed_by:
            lines.append(f"   _Подтверждено:_ {', '.join(confirmed_by)}")
        note = item.get("note")
        if note:
            lines.append(f"   _{note}_")
        lines.append("")

    return "\n".join(lines)

async def send_report(items: list[dict]):
    text = build_report_text(items)
    MAX_LEN = 4000
    for i in range(0, len(text), MAX_LEN):
        await bot.send_message(
            chat_id=config.TG_REPORT_CHAT_ID,
            text=text[i:i + MAX_LEN],
            parse_mode=ParseMode.MARKDOWN,
        )
    print("[reporter] Отчёт отправлен.")