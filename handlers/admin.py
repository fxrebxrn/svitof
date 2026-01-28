import re
from datetime import date
from aiogram import types
from config import ADMIN_ID
from db import get_db
from scheduler import rebuild_jobs

TIME_RE = re.compile(r"(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}|24:00)")


async def upload_command(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer(
        "📥 Надішліть графік одним повідомленням текстом.\n"
        "Формат: ЦЕК / ДТЕК → Черги → Час"
    )


async def handle_text_schedule(message: types.Message, bot):
    if message.from_user.id != ADMIN_ID:
        return

    lines = [l.strip() for l in message.text.splitlines() if l.strip()]
    company = lines[0].upper()
    today = date.today().isoformat()

    current_queue = None
    added = 0

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "DELETE FROM schedules WHERE company=? AND date=?",
        (company, today)
    )

    for line in lines[1:]:
        if line.lower().startswith(("черга", "група")):
            current_queue = line.split()[-1]
            continue

        if not current_queue:
            continue

        clean = re.sub(r"\(.*?\)", "", line)
        m = TIME_RE.search(clean)
        if not m:
            continue

        off_t, on_t = m.groups()

        cur.execute("""
            INSERT INTO schedules
            (company, queue, date, off_time, on_time)
            VALUES (?, ?, ?, ?, ?)
        """, (company, current_queue, today, off_t, on_t))

        added += 1

    db.commit()
    db.close()

    rebuild_jobs(bot)

    await message.answer(
        f"✅ Графік збережено\n"
        f"Компанія: {company}\n"
        f"Інтервалів: {added}"
    )
