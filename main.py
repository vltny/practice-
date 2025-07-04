import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router


bot = Bot(token="8035852822:AAGZLzOW_cmLxcYL-NM2JYXLA5kd-_6ZnDc")
dp = Dispatcher()


async def main():
    dp.include_router(router=router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
