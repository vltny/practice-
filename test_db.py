import asyncio
import asyncpg
import os
from dotenv import load_dotenv


load_dotenv()

async def test_connection():
    try:
        conn = await asyncpg.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        print("✅ Подключение к БД успешно!")
        
        # Проверка таблиц
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        print("\nТаблицы в базе:")
        for table in tables:
            print(f"- {table['table_name']}")
            
        await conn.close()
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

asyncio.run(test_connection())