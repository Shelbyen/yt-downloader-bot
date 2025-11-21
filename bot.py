from argparse import ArgumentParser
import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

from src.config import project_settings
from src.handlers import routers


async def on_startup():
    """ Startup function """
    print('Бот вышел в онлайн')


def setup_logging():
    """ Base logging setup """
    logging.basicConfig(
        level=logging.INFO,
        filename=f"logs/{project_settings.VERSION}_{datetime.now().strftime('%d%m%Y_%H%M%S')}.log",
        filemode="w",
        format="%(asctime)s %(levelname)s %(message)s",
        encoding='utf-8'
    )


async def main(use_api_server: bool = True, address: str = 'localhost', port: int = 8081):
    """ Connect to telegram api server and start all bot """
    session = None
    if use_api_server:
        session = AiohttpSession(
            api=TelegramAPIServer.from_base(f"http://{address}:{port}", is_local=True)
        )
    bot = Bot(token=project_settings.TOKEN, session=session)
    dp = Dispatcher()

    dp.include_routers(*routers)

    dp.startup.register(on_startup)

    await bot.delete_webhook(drop_pending_updates=True)
    setup_logging()
    await dp.start_polling(bot)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--use_server", type=str, default='True',
                        choices=('True', 'False'),
                        help="Use Telegram API Server?"
                        )   # Argparser does not know how to work with bool
    parser.add_argument("--address", type=str, default='localhost',
                        help="Address Telegram API Server"
                        )
    parser.add_argument("--port", type=int, default=8081,
                        help="Port Telegram API Server"
                        )
    args = parser.parse_args()
    use_server = args.use_server == 'True'
    asyncio.run(main(use_server, args.address, args.port))
