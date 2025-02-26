import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.enums import ChatAction

from classes import ai_client
from keyboards import *
from keyboards.callback_data import QuizData
from .command_handlers import com_start
from fsm.states import ChatGPTStates, CelebrityDialog, QuizGame

ai_handler = Router()


@ai_handler.message(F.text == 'Хочу еще факт')
@ai_handler.message(Command('random'))
@ai_handler.message(F.text == 'Рандомный факт')
async def ai_random_fact(message: Message):
    await message.bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )
    request_message = [
        {
            'role': 'user',
            'content': 'Напиши рандомный факт',
        }
    ]
    caption = await ai_client.text_request(request_message, 'random.txt')
    photo_file = FSInputFile(path=os.path.join('images', 'random.jpg'))
    await message.answer_photo(
        photo=photo_file,
        caption=caption,
        reply_markup=kb_random_facts(),
    )


@ai_handler.message(ChatGPTStates.wait_for_request)
async def ai_gpt_request(message: Message, state: FSMContext):
    if message.text == 'Назад':
        await com_start(message)
    else:
        request = message.text
        await message.bot.send_chat_action(
            chat_id=message.from_user.id,
            action=ChatAction.TYPING,
        )
        message_list = [
            {'role': 'user',
             'content': request}
        ]
        photo_file = FSInputFile(path=os.path.join('images', 'gpt.jpg'))
        caption = await ai_client.text_request(message_list, 'gpt.txt')
        await message.answer_photo(
            photo=photo_file,
            caption=caption,
            reply_markup=kb_start(),
        )
    await state.clear()


@ai_handler.message(CelebrityDialog.wait_for_answer)
async def celebrity_answer(message: Message, state: FSMContext):
    user_text = 'Пока, всего тебе хорошего!' if message.text == 'Попрощаться' else message.text
    data = await state.get_data()
    user_request = {
        'role': 'user',
        'content': user_text,
    }
    data['dialog'].append(user_request)
    celebrity_response = await ai_client.text_request(data['dialog'], data['prompt'] + '.txt')
    celebrity_response_dict = {
        'role': 'assistant',
        'content': celebrity_response,
    }
    data['dialog'].append(celebrity_response_dict)
    photo_file = FSInputFile(path=os.path.join('images', data['prompt'] + '.jpg'))
    await state.update_data(dialog=data['dialog'])
    await message.answer_photo(
        photo=photo_file,
        caption=celebrity_response,
        reply_markup=kb_say_goodbye(),
    )
    if message.text == 'Попрощаться':
        await state.clear()
        await com_start(message)



@ai_handler.callback_query(QuizData.filter(F.button == 'select_quiz'))
async def quiz_get_question(callback: CallbackQuery, callback_data: QuizData, state: FSMContext):
    data = await state.get_data()
    data['score'] = data.get('score', 0)
    if callback_data.subject != 'quiz_more':
        data['type'] = callback_data.subject
    message_list = [
        {'role': 'user',
         'content': data['type']}
    ]
    ai_question = await ai_client.text_request(message_list, 'quiz.txt')
    photo_file = FSInputFile(path=os.path.join('images', 'quiz.jpg'))
    data['question'] = ai_question
    await state.update_data(data)
    await callback.bot.send_photo(
        chat_id=callback.from_user.id,
        photo=photo_file,
        caption=ai_question,
    )
    await state.set_state(QuizGame.wait_for_answer)


@ai_handler.message(QuizGame.wait_for_answer)
async def quiz_correct_answer(message: Message, state: FSMContext):
    user_answer = message.text
    await message.bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )
    data = await state.get_data()
    message_list = [
        {'role': 'assistant',
         'content': data['question']},
        {'role': 'user',
         'content': user_answer}
    ]
    ai_answer = await ai_client.text_request(message_list, 'quiz.txt')
    photo_file = FSInputFile(path=os.path.join('images', 'quiz.jpg'))
    correct_answer = ai_answer.split(' ', 1)[0]
    if correct_answer == 'Правильно!':
        data['score'] += 1
        await state.update_data(score=data['score'])
    await message.answer_photo(
        photo=photo_file,
        caption=ai_answer + f'\nВаш текущий счет: {data['score']}',
        reply_markup=ikb_next_quiz(),
    )
    await state.set_state(QuizGame.quiz_next_step)
