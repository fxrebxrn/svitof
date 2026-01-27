from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

company_kb = ReplyKeyboardMarkup(resize_keyboard=True)
company_kb.add(
    KeyboardButton("ДТЕК"),
    KeyboardButton("ЦЕК")
)
