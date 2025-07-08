import json
from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
import app.keyboards as kb
from app.additional import updateMenu

router = Router()
user_state = {}


@router.message(CommandStart())
async def cmd_help(message: Message):
    await message.answer('Добро пожаловать в бота КТЗ', reply_markup=kb.main)


@router.message(F.text == 'Новости')
async def handle_message_news(message: Message):
    await message.answer('Выберите тип отображения', reply_markup=kb.news)


@router.message(F.text == 'Меню столовой')
async def handle_message_menu(message: Message):
    file = FSInputFile('data/test.pdf')
    await message.answer_document(document=file, caption='Меню столовой')
    await message.answer(updateMenu())


@router.message(F.text == 'Транспорт')
async def handle_message_transport(message: Message):
    await message.answer("Транспорт в разработке")


@router.message(F.text == 'Соц. программы')
async def handle_message_social(message: Message):
    await message.answer("Социальные программы в разработке")


@router.message(F.text == 'Опрос')
async def handle_message_survey(message: Message):
    await message.answer("Опросы в разработке")


@router.message(F.text == 'Вопрос к руководству')
async def handle_message_ask(message: Message):
    await message.answer("Вопросы к руководству в разработке")




@router.message(F.text == 'Последние новости')
async def handle_message_last_news(message: Message):
    user_id = message.from_user.id
    user_state[user_id] = {'waiting_number': True,
                           'category': 'all'}
    await message.answer('Сколько новостей вы хотите посмотреть?')


@router.message(F.text == 'Категории')
async def handle_message_categories(message: Message):
    await message.answer('Выберите категорию', reply_markup=kb.newsCategories)


@router.message(F.text == 'Праздники')
async def handle_news_holidays(message: Message):
    user_id = message.from_user.id
    user_state[user_id] = {'waiting_number': True,
                           'category': 'Праздники'}
    await message.answer('Сколько новостей вы хотите посмотреть?')


@router.message(F.text == 'Жизнь завода')
async def handle_news_life(message: Message):
    user_id = message.from_user.id
    user_state[user_id] = {'waiting_number': True,
                           'category': 'Жизнь завода'}
    await message.answer('Сколько новостей вы хотите посмотреть?')


@router.message(F.text == 'Вакансии')
async def handle_news_vacancies(message: Message):
    user_id = message.from_user.id
    user_state[user_id] = {'waiting_number': True,
                           'category': 'Вакансии'
    }
    await message.answer('Сколько новостей вы хотите посмотреть?')


@router.message(F.text == 'Сотрудники')
async def handle_news_employees(message: Message):
    user_id = message.from_user.id
    user_state[user_id] = {'waiting_number': True,
                           'category': 'Сотрудники'}
    await message.answer('Сколько новостей вы хотите посмотреть?')


@router.message(F.text == 'Изобретения')
async def handle_news_inventions(message: Message):
    user_id = message.from_user.id
    user_state[user_id] = {'waiting_number': True,
                           'category': 'Изобретения'}
    await message.answer('Сколько новостей вы хотите посмотреть?')


@router.message(F.text == 'Достижения')
async def handle_news_achievements(message: Message):
    user_id = message.from_user.id
    user_state[user_id] = {'waiting_number': True,
                           'category': 'Достижения'}
    await message.answer('Сколько новостей вы хотите посмотреть?')


@router.message(lambda m: m.text.isdigit())
async def handle_news_number(message: Message):
    user_id = message.from_user.id
    if user_id not in user_state or not user_state[user_id].get('waiting_number'):
        return

    number = int(message.text)
    user_state[user_id]['number'] = number
    user_state[user_id]['waiting_number'] = False

    await message.answer(f"Вы ввели число: {user_state[user_id]['number']}, Выбранная категория: {user_state[user_id]['category']}")
    with open('data/news.json', 'r') as f:
        allNews = json.load(f)
        if(user_state[user_id]['category'] == 'all'):
            filtered = allNews
        else:
            filtered = [n for n in allNews if n["category"] == user_state[user_id]['category']]

        selected = filtered[:user_state[user_id]['number']]

        if not selected:
            await message.answer("К сожалению, новостей в этой категории нет.", reply_markup=kb.main)
        else:
            for news in selected:
                await message.answer(
                    f"<i>{news['category']}</i>\n\n{news['text']}\n\n<b>{news['date']}</b>",
                    parse_mode="HTML", reply_markup=kb.main
                )

        user_state.pop(user_id)
