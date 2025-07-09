from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🔍 Новости'), KeyboardButton(text='🍽 Меню столовой')],
    [KeyboardButton(text='🚍 Транспорт'), KeyboardButton(text='🪪 Соц. программы')],
    [KeyboardButton(text='📊 Опрос'), KeyboardButton(text='📤 Задать вопрос')]
], resize_keyboard=True)

news = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🚀 Последние новости'), KeyboardButton(text='🧩 Категории')],
    [KeyboardButton(text='◀️ Назад')]
], resize_keyboard=True)

newsCategories = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🎉 Праздники'), KeyboardButton(text='🏭 Жизнь завода')],
    [KeyboardButton(text='💼 Вакансии'), KeyboardButton(text='👨‍🔧 Сотрудники')],
    [KeyboardButton(text='🦾 Изобретения'), KeyboardButton(text='🏆 Достижения')],
    [KeyboardButton(text='◀️ Назад')]
], resize_keyboard=True)
