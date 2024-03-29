from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import logging
import os
from handlers import default_handlers, help_handlers, tutor_handlers, alarm_handlers, command_handlers
import db


async def main():
    db.create_table()
    bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(tutor_handlers.router, help_handlers.router,
                       command_handlers.router, alarm_handlers.router, default_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
