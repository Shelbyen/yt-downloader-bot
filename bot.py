import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

from src.config import project_settings
from src.handlers import routers


async def on_startup():
    print('Бот вышел в онлайн')


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        filename=f"logs/{project_settings.VERSION}_{datetime.now().strftime('%d%m%Y_%H%M%S')}.log",
        filemode="w",
        format="%(asctime)s %(levelname)s %(message)s",
        encoding='utf-8'
    )


async def main():
    session = AiohttpSession(api=TelegramAPIServer.from_base("http://localhost:8081", is_local=True))
    bot = Bot(token=project_settings.TOKEN, session=session)
    dp = Dispatcher()

    dp.include_routers(*routers)

    dp.startup.register(on_startup)

    await bot.delete_webhook(drop_pending_updates=True)
    setup_logging()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
