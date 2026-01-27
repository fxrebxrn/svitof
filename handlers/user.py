from aiogram import types
from db import get_conn
from keyboards.queue import queue_kb

async def company_handler(message: types.Message):
    company = message.text

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (message.from_user.id,)
        )
        cur.execute(
            "UPDATE users SET company=? WHERE user_id=?",
            (company, message.from_user.id)
        )
        conn.commit()

    await message.answer(
        "Дякуємо.\nБудь ласка, оберіть Вашу чергу:",
        reply_markup=queue_kb
    )


async def queue_handler(message: types.Message):
    queue = message.text

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET queue=? WHERE user_id=?",
            (queue, message.from_user.id)
        )
        conn.commit()

    await message.answer(
        "✅ Налаштування збережено.\n\n"
        "Ви отримуватимете сповіщення:\n"
        "• за 10 хвилин до вимкнення\n"
        "• у момент вимкнення\n"
        "• за 10 хвилин до включення\n"
        "• у момент включення електроенергії"
    )
