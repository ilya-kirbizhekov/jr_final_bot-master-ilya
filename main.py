import asyncio
import os

from aiogram import Bot, Dispatcher

from handlers import all_handlers_router


def on_start():
    print('Bot is started...')


def on_shutdown():
    print('Bot is down now...')


async def start_bot():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.startup.register(on_start)
    dp.shutdown.register(on_shutdown)
    dp.include_routers(
        all_handlers_router,
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass
