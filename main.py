import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.token import tok


bot = Bot(token=tok)
dp = Dispatcher()


async def main():
    dp.include_router(router=router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
