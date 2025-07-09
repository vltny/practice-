import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.database import db

#bot = Bot(token="7865753586:AAEXAhxKNr0VpDC2d_g4Qg1y4yJNNOijzQs") 
bot = Bot(token="8035852822:AAGZLzOW_cmLxcYL-NM2JYXLA5kd-_6ZnDc")
dp = Dispatcher()

async def main():
    await db.create_pool()
    dp.include_router(router=router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
