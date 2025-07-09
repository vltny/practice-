import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

class Database:
    def __init__(self):
        self.pool = None

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )

    async def get_user_by_personnel_number(self, personnel_number: str):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(
                'SELECT * FROM "user" WHERE personnel_number = $1', 
                personnel_number
            )
    
    async def get_user_by_phone_number(self, phone_number: str):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(
                'SELECT * FROM "user" WHERE phone_number = $1', 
                phone_number
            )
    
    async def create_user(self, username: str, personnel_number: str = None, phone_number: str = None):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(
                '''INSERT INTO "user" (username, personnel_number, phone_number) 
                VALUES ($1, $2, $3) RETURNING *''',
                username, personnel_number, phone_number
            )

db = Database()