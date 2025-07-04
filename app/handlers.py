import os
from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command, CommandStart
import app.keyboards as kb

router = Router()


@router.message(CommandStart())
async def cmd_help(message: Message):
    await message.answer('Добро пожаловать в бота КТЗ', reply_markup=kb.main)


@router.message(F.text == 'Новости')
async def handle_message(message: Message):
    await message.answer('Новости в разработке', reply_markup=kb.news)


@router.message(F.text == 'Меню столовой')
async def handle_message(message: Message):
    file = FSInputFile('data/test.pdf')
    await message.answer_document(document=file, caption='Меню столовой')


@router.message(F.text == 'Транспорт')
async def handle_message(message: Message):
    await message.answer("Транспорт в разработке")


@router.message(F.text == 'Соц. программы')
async def handle_message(message: Message):
    await message.answer("Социальные программы в разработке")


@router.message(F.text == 'Опрос')
async def handle_message(message: Message):
    await message.answer("Опросы в разработке")


@router.message(F.text == 'Вопрос к руководству')
async def handle_message(message: Message):
    await message.answer("Вопросы к руководству в разработке")


@router.message(F.text == 'Последние новости')
async def handle_message(message: Message):
    n = int(message.text)
    print(n)
    await message.answer('Сколько новостей вы хотите посмотреть?')


@router.message(F.text == 'Категории')
async def handle_message(message: Message):
    await message.answer('Выберите категорию', reply_markup=kb.newsCategories)


@router.message(F.text == 'Праздники')
async def handle_message(message: Message):
    await message.answer('Сколько новостей вы хотите посмотреть?')


@router.message(F.text == 'Жизнь завода')
async def handle_message(message: Message):
    await message.answer('Сколько новостей вы хотите посмотреть?')


@router.message(F.text == 'Вакансии')
async def handle_message(message: Message):
    await message.answer('Сколько новостей вы хотите посмотреть?')


@router.message(F.text == 'Сотрудники')
async def handle_message(message: Message):
    await message.answer('Сколько новостей вы хотите посмотреть?')


@router.message(F.text == 'Изобретения')
async def handle_message(message: Message):
    await message.answer('Сколько новостей вы хотите посмотреть?')


@router.message(F.text == 'Достижения')
async def handle_message(message: Message):
    await message.answer('Сколько новостей вы хотите посмотреть?')
