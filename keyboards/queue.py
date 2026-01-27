from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

queues = [
    "1.1","1.2","2.1","2.2","3.1","3.2",
    "4.1","4.2","5.1","5.2","6.1","6.2"
]

queue_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
queue_kb.add(*[KeyboardButton(q) for q in queues])
