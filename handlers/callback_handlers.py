import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.enums import ChatAction

from classes import ai_client
from keyboards.reply_keyboards import kb_random_facts, kb_start, kb_back
from .command_handlers import com_start
from fsm.states import CelebrityDialog
from keyboards.callback_data import CelebrityData, QuizData

callback_router = Router()


@callback_router.callback_query(CelebrityData.filter(F.button == 'cb'))
async def select_celebrity(callback: CallbackQuery, callback_data: CelebrityData, state: FSMContext):
    await state.set_state(CelebrityDialog.wait_for_answer)
    await state.update_data(name=callback_data.name, dialog=[], prompt=callback_data.file_name)
    photo_file = FSInputFile(path=os.path.join('images', callback_data.file_name + '.jpg'))
    await callback.bot.send_photo(
        chat_id=callback.from_user.id,
        photo=photo_file,
        caption=f'Вас приветствует {callback_data.name}!\nЗадайте вопрос первым:',
        reply_markup=kb_back(),
    )



