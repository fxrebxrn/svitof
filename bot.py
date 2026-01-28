from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
from db import init_db
from scheduler import scheduler
from handlers.start import start_handler
from handlers.user import company_handler, queue_handler
from handlers.admin import upload_command, handle_file

bot = Bot(TOKEN)
dp = Dispatcher(bot)

dp.register_message_handler(start_handler, commands=["start"])
dp.register_message_handler(company_handler, text=["ДТЕК", "ЦЕК"])
dp.register_message_handler(queue_handler, regexp=r"^\d\.\d$")
dp.register_message_handler(upload_command, commands=["upload"])
dp.register_message_handler(
    lambda m: m.document is not None,
    lambda m: handle_file(m, bot),
    content_types=types.ContentType.DOCUMENT
)

async def on_startup(dp):
    init_db()
    scheduler.start()
    print("✅ Бот запущено, scheduler активний")

if __name__ == "__main__":
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup
    )
dp.register_message_handler(
    handle_text_schedule,
    lambda m: m.from_user.id == ADMIN_ID,
    content_types=types.ContentType.TEXT
)
