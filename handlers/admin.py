import re
from datetime import date
from db import get_conn
from scheduler import reschedule
from config import ADMIN_ID


TIME_RE = re.compile(r"(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}|24:00)")


async def handle_schedule_text(message, bot):
    if message.from_user.id != ADMIN_ID:
        return

    lines = [l.strip() for l in message.text.splitlines() if l.strip()]
    if not lines:
        return

    company = lines[0].upper()
    today = date.today().isoformat()

    current_queue = None
    inserted = 0

    with get_conn() as conn:
        cur = conn.cursor()

        # видаляємо старі графіки компанії
        cur.execute(
            "DELETE FROM schedules WHERE company=? AND date=?",
            (company, today)
        )

        for line in lines[1:]:
            # Черга / Група
            if line.lower().startswith(("черга", "група")):
                current_queue = line.split()[-1]
                continue

            if not current_queue:
                continue

            # прибираємо коментарі в дужках
            clean_line = re.sub(r"\(.*?\)", "", line)

            match = TIME_RE.search(clean_line)
            if not match:
                continue

            start, end = match.groups()

            cur.execute(
                """
                INSERT INTO schedules
                (company, queue, date, off_time, on_time)
                VALUES (?, ?, ?, ?, ?)
                """,
                (company, current_queue, today, start, end)
            )
            inserted += 1

        conn.commit()

    reschedule(bot)

    await message.answer(
        f"✅ Графік збережено\n"
        f"Компанія: {company}\n"
        f"Додано інтервалів: {inserted}\n"
        f"Сповіщення оновлено"
    )
