from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta, date
from db import get_db
from bot import bot  # ⚠️ це безпечно, бо bot ініціалізується раніше

scheduler = AsyncIOScheduler()


def rebuild_jobs(bot):
    scheduler.remove_all_jobs()
    now = datetime.now()

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT u.user_id, s.off_time, s.on_time
        FROM schedules s
        JOIN users u
          ON u.company=s.company AND u.queue=s.queue
        WHERE s.date=?
    """, (date.today().isoformat(),))

    for user_id, off_t, on_t in cur.fetchall():
        off_dt = datetime.combine(date.today(), parse_time(off_t))
        on_dt = datetime.combine(date.today(), parse_time(on_t))

        if off_dt - timedelta(minutes=10) > now:
            scheduler.add_job(
                send,
                "date",
                run_date=off_dt - timedelta(minutes=10),
                args=[user_id, "⚠️ Через 10 хвилин буде відключення електроенергії"]
            )

        if off_dt > now:
            scheduler.add_job(
                send,
                "date",
                run_date=off_dt,
                args=[user_id, "🔴 Електроенергію вимкнено"]
            )

        if on_dt > now:
            scheduler.add_job(
                send,
                "date",
                run_date=on_dt,
                args=[user_id, "🟢 Електроенергію відновлено"]
            )

    db.close()


async def send(user_id, text):
    await bot.send_message(user_id, text)


def parse_time(t):
    if t == "24:00":
        return datetime.strptime("23:59", "%H:%M").time()
    return datetime.strptime(t, "%H:%M").time()
