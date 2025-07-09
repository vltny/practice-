import json
from aiogram import F, Router
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import app.keyboards as kb
from app.additional import updateMenu
from app.database import db

router = Router()
user_state = {}

class AuthState(StatesGroup):
    WAITING_FOR_PERSONNEL_NUMBER = State()
    WAITING_FOR_PHONE_NUMBER = State()
    WAITING_FOR_USERNAME = State()  # Для запроса имени

# Проверка аутентификации пользователя
async def check_auth(message: Message, state: FSMContext) -> bool:
    current_state = await state.get_state()
    if current_state not in [AuthState.WAITING_FOR_PERSONNEL_NUMBER.state, 
                            AuthState.WAITING_FOR_PHONE_NUMBER.state,
                            AuthState.WAITING_FOR_USERNAME.state]:
        return True

    await message.answer("⚠️ Сначала пройдите аутентификацию через /start")
    return False

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Добро пожаловать! Выберите вариант входа:", reply_markup=kb.start)

@router.message(F.text == 'У меня есть табельный номер')
async def has_personnel_number(message: Message, state: FSMContext):
    await message.answer("Введите ваш табельный номер:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AuthState.WAITING_FOR_PERSONNEL_NUMBER)

@router.message(F.text == 'У меня нет табельного номера')
async def no_personnel_number(message: Message, state: FSMContext):
    await message.answer("Введите ваш номер телефона:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AuthState.WAITING_FOR_PHONE_NUMBER)

@router.message(AuthState.WAITING_FOR_PERSONNEL_NUMBER)
async def process_personnel_number(message: Message, state: FSMContext):
    personnel_number = message.text.strip()
    user = await db.get_user_by_personnel_number(personnel_number)

    if user:
        await message.answer(f"Добро пожаловать, {user['username']}!", reply_markup=kb.main)
        await state.clear()
    else:
        await state.update_data(personnel_number=personnel_number)
        await message.answer("Табельный номер не найден. Введите ваш номер телефона:")
        await state.set_state(AuthState.WAITING_FOR_PHONE_NUMBER)

@router.message(AuthState.WAITING_FOR_PHONE_NUMBER)
async def process_phone_number(message: Message, state: FSMContext):
    phone_number = message.text.strip()
    user = await db.get_user_by_phone_number(phone_number)

    if user:
        await message.answer(f"Добро пожаловать, {user['username']}!", reply_markup=kb.main)
        await state.clear()
    else:
        data = await state.get_data()
        personnel_number = data.get('personnel_number')

        await state.update_data(phone_number=phone_number)
        await message.answer("Регистрация. Как к вам обращаться?")
        await state.set_state(AuthState.WAITING_FOR_USERNAME)

@router.message(AuthState.WAITING_FOR_USERNAME)
async def process_username(message: Message, state: FSMContext):
    username = message.text.strip()
    data = await state.get_data()

    # Создаем нового пользователя
    user = await db.create_user(
        username=username,
        personnel_number=data.get('personnel_number'),
        phone_number=data.get('phone_number')
    )

    if user:
        await message.answer(f"Приятно познакомиться, {username}! Ваши данные сохранены.", reply_markup=kb.main)
    else:
        await message.answer("❌ Ошибка при создании профиля. Попробуйте снова через /start")

    await state.clear()

@router.message(F.text == '🔍 Новости')
async def handle_message_news(message: Message, state: FSMContext):
    if not await check_auth(message, state):
        return
    await message.answer('Выберите тип отображения', reply_markup=kb.news)


@router.message(F.text == '🍽 Меню столовой')
async def handle_message_menu(message: Message, state: FSMContext):
    if not await check_auth(message, state):
        return
    menu_lines = updateMenu()
    text = ""

    for line in menu_lines:
        if (len(text) + len(line) > 4000) or ('|' in line):
            line = ''
            await message.answer(text, parse_mode="HTML")
            text = ""
        text += line

    if text:
        await message.answer(text, parse_mode="HTML", reply_markup=kb.menu)


@router.message(F.text == '🗓 Меню на неделю')
async def handle_message_transport(message: Message, state: FSMContext):
    if not await check_auth(message, state):
        return
    file = FSInputFile('data/Menu.pdf')
    await message.answer_document(document=file, caption='Меню столовой')


@router.message(F.text == '🚍 Транспорт')
async def handle_message_transport(message: Message, state: FSMContext):
    if not await check_auth(message, state):
        return
    await message.answer("Транспорт в разработке")


@router.message(F.text == '🪪 Соц. программы')
async def handle_message_social(message: Message, state: FSMContext):
    if not await check_auth(message, state):
        return
    await message.answer("Социальные программы в разработке")


@router.message(F.text == '📊 Опрос')
async def handle_message_survey(message: Message, state: FSMContext):
    if not await check_auth(message, state):
        return
    await message.answer("Опросы в разработке")


@router.message(F.text == '📤 Задать вопрос')
async def handle_message_ask(message: Message, state: FSMContext):
    if not await check_auth(message, state):
        return
    await message.answer("Вопросы к руководству в разработке")

@router.message(F.text == '◀️ Назад')
async def handle_message_back(message: Message, state: FSMContext):
    if not await check_auth(message, state):
        return
    await message.answer("Возврат в меню", reply_markup=kb.main)


@router.message(F.text == '🚀 Последние новости')
async def handle_message_last_news(message: Message, state: FSMContext):
    if not await check_auth(message, state):
        return
    user_id = message.from_user.id
    user_state[user_id] = {'waiting_number': True,
                           'category': 'all'}
    await message.answer('Сколько новостей вы хотите посмотреть?')


@router.message(F.text == '🧩 Категории')
async def handle_message_categories(message: Message, state: FSMContext):
    if not await check_auth(message, state):
        return
    await message.answer('Выберите категорию', reply_markup=kb.newsCategories)


@router.message(F.text == '🎉 Праздники')
async def handle_news_holidays(message: Message, state: FSMContext):
    if not await check_auth(message, state):
        return
    user_id = message.from_user.id
    user_state[user_id] = {'waiting_number': True,
                           'category': 'Праздники'}
    await message.answer('Сколько новостей вы хотите посмотреть?')


@router.message(F.text == '🏭 Жизнь завода')
async def handle_news_life(message: Message, state: FSMContext):
    if not await check_auth(message, state):
        return
    user_id = message.from_user.id
    user_state[user_id] = {'waiting_number': True,
                           'category': 'Жизнь завода'}
    await message.answer('Сколько новостей вы хотите посмотреть?')


@router.message(F.text == '💼 Вакансии')
async def handle_news_vacancies(message: Message, state: FSMContext):
    if not await check_auth(message, state):
        return
    user_id = message.from_user.id
    user_state[user_id] = {'waiting_number': True,
                           'category': 'Вакансии'
    }
    await message.answer('Сколько новостей вы хотите посмотреть?')


@router.message(F.text == '👨‍🔧 Сотрудники')
async def handle_news_employees(message: Message, state: FSMContext):
    if not await check_auth(message, state):
        return
    user_id = message.from_user.id
    user_state[user_id] = {'waiting_number': True,
                           'category': 'Сотрудники'}
    await message.answer('Сколько новостей вы хотите посмотреть?')


@router.message(F.text == '🦾 Изобретения')
async def handle_news_inventions(message: Message, state: FSMContext):
    if not await check_auth(message, state):
        return
    user_id = message.from_user.id
    user_state[user_id] = {'waiting_number': True,
                           'category': 'Изобретения'}
    await message.answer('Сколько новостей вы хотите посмотреть?')


@router.message(F.text == '🏆 Достижения')
async def handle_news_achievements(message: Message, state: FSMContext):
    if not await check_auth(message, state):
        return
    user_id = message.from_user.id
    user_state[user_id] = {'waiting_number': True,
                           'category': 'Достижения'}
    await message.answer('Сколько новостей вы хотите посмотреть?')


@router.message(lambda m: m.text.isdigit())
async def handle_news_number(message: Message, state: FSMContext):
    if not await check_auth(message, state):
        return
    user_id = message.from_user.id
    if user_id not in user_state or not user_state[user_id].get('waiting_number'):
        return

    number = int(message.text)
    if number < 1:
        await message.answer('Неверное число')
        return
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
