from aiogram import types
from keyboards.company import company_kb

async def start_handler(message: types.Message):
    await message.answer(
        "Вітаємо!\n\n"
        "Цей бот повідомляє про відключення та включення електроенергії "
        "згідно з офіційними графіками.\n\n"
        "Будь ласка, оберіть Вашу енергокомпанію:",
        reply_markup=company_kb
    )
