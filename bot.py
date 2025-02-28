import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher

from src.config.project_config import settings
from src.handlers import routers


async def on_startup():
    print('Бот вышел в онлайн')


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        filename=f"logs/{settings.VERSION}_{datetime.now().strftime('%d%m%Y_%H%M%S')}.log",
        filemode="w",
        format="%(asctime)s %(levelname)s %(message)s",
        encoding='utf-8'
    )


async def main():
    bot = Bot(token=settings.TOKEN)
    dp = Dispatcher()

    dp.include_routers(*routers)

    dp.startup.register(on_startup)

    await bot.delete_webhook(drop_pending_updates=True)
    setup_logging()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
