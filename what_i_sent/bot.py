from aiogram import Router, Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import asyncio
import logging
import sys
from configparser import ConfigParser

from handlers import rt

dp = Dispatcher()
dp.include_router(rt)


async def main() -> None:
    parser = ConfigParser()
    parser.read('keys.ini')
    token = parser['Bot']['token']

    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())