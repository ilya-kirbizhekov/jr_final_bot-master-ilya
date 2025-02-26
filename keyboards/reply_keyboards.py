from aiogram.utils.keyboard import ReplyKeyboardBuilder


def kb_start():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(
        text='Рандомный факт',
    )
    keyboard.button(
        text='Запрос к GPT',
    )
    keyboard.button(
        text='Диалог с личностью'
    )
    keyboard.button(
        text='QUIZ!'
    )
    keyboard.button(
        text='Помощь',
    )
    keyboard.adjust(2, 2, 1)
    return keyboard.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Выберите пункт меню...'
    )


def kb_random_facts():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(
        text='Хочу еще факт',
    )
    keyboard.button(
        text='Закончить',
    )
    return keyboard.as_markup(
        resize_keyboard=True,
    )


def kb_back():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(
        text='Назад',
    )
    return keyboard.as_markup(
        resize_keyboard=True,
    )


def kb_say_goodbye():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(
        text='Попрощаться',
    )
    return keyboard.as_markup(
        resize_keyboard=True,
    )

