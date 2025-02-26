import os
from collections import namedtuple
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callback_data import CelebrityData, QuizData


def ikb_celebrity():
    Celebrity = namedtuple('Celebrity', ['name', 'file_name'])
    keyboard = InlineKeyboardBuilder()
    file_list = [file for file in os.listdir('prompts') if file.startswith('talk_')]
    celebrity_list = []
    for file in file_list:
        with open(os.path.join('prompts', file), 'r', encoding='UTF-8') as txt_file:
            name = txt_file.read().split(',', 1)[0][5:].title()
            celebrity_list.append(Celebrity(name, file.rsplit('.', 1)[0]))
    for celebrity in celebrity_list:
        keyboard.button(
            text=celebrity.name,
            callback_data=CelebrityData(
                button='cb',
                name=celebrity.name,
                file_name=celebrity.file_name,
            ),
        )
    keyboard.adjust(*[1] * len(file_list))
    return keyboard.as_markup()


def ikb_select_subject_quiz():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        ('Программирование', 'quiz_prog'),
        ('Математика', 'quiz_math'),
        ('Биология', 'quiz_biology'),
        ('Назад', 'quiz_back')
    ]
    for button in buttons:
        keyboard.button(
            text=button[0],
            callback_data=QuizData(
                button='select_quiz',
                subject=button[1],
            )
        )
    keyboard.adjust(*[1] * len(buttons))
    return keyboard.as_markup()


def ikb_next_quiz():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text='Хочу еще вопрос!',
        callback_data=QuizData(
            button='select_quiz',
            subject='quiz_more',
        )
    )
    keyboard.button(
        text='Сменить тему',
        callback_data=QuizData(
            button='select_type',
            subject='',
        )
    )
    keyboard.button(
        text='Закончить',
        callback_data=QuizData(
            button='select_quiz',
            subject='quiz_back',
        )
    )
    keyboard.adjust(1, 1, 1)
    return keyboard.as_markup(
        resize_keyboard=True,
    )
