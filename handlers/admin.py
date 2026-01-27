from aiogram import types
import pandas as pd
from config import ADMIN_ID
from db import get_conn
from scheduler import reschedule

async def upload_command(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "Будь ласка, надішліть Excel-файл з графіками.\n\n"
        "Формат колонок:\n"
        "company | queue | date | off_time | on_time"
    )

async def handle_file(message: types.Message, bot):
    if message.from_user.id != ADMIN_ID:
        return

    file = await bot.download_file_by_id(message.document.file_id)
    df = pd.read_excel(file)

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM schedules")

        for _, row in df.iterrows():
            cur.execute("""
            INSERT INTO schedules (company, queue, date, off_time, on_time)
            VALUES (?, ?, ?, ?, ?)
            """, (
                row["company"],
                row["queue"],
                str(row["date"]),
                row["off_time"],
                row["on_time"]
            ))
        conn.commit()

    reschedule(bot)

    await message.answer(
        "✅ Графіки успішно оновлено.\n"
        "Усі сповіщення автоматично перераховано."
    )
