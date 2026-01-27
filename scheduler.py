from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from db import get_conn

scheduler = AsyncIOScheduler()

async def send_message(bot, user_id, text):
    try:
        await bot.send_message(user_id, text)
    except:
        pass

def reschedule(bot):
    scheduler.remove_all_jobs()

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
        SELECT u.user_id, s.company, s.queue, s.date, s.off_time, s.on_time
        FROM users u
        JOIN schedules s
        ON u.company = s.company AND u.queue = s.queue
        """)

        rows = cur.fetchall()

    for user_id, company, queue, date, off_t, on_t in rows:
        off_dt = datetime.fromisoformat(f"{date} {off_t}")
        on_dt = datetime.fromisoformat(f"{date} {on_t}")

        scheduler.add_job(
            send_message, "date",
            run_date=off_dt - timedelta(minutes=10),
            args=[bot, user_id, f"⏰ Через 10 хвилин планове відключення електроенергії (черга {queue})."]
        )

        scheduler.add_job(
            send_message, "date",
            run_date=off_dt,
            args=[bot, user_id, f"⚡ Згідно з графіком, електроенергію вимкнено (черга {queue})."]
        )

        scheduler.add_job(
            send_message, "date",
            run_date=on_dt - timedelta(minutes=10),
            args=[bot, user_id, f"⏰ Через 10 хвилин планове включення електроенергії (черга {queue})."]
        )

        scheduler.add_job(
            send_message, "date",
            run_date=on_dt,
            args=[bot, user_id, f"💡 Згідно з графіком, електроенергія повинна з’явитися (черга {queue})."]
        )

    if not scheduler.running:
        scheduler.start()
