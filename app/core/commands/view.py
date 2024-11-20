from aiogram import Router
from aiogram.filters.command import Command

from app.core.modules.util import *


router = Router()


@router.message(Command("view"))
async def get(message: types.Message):
    test_id = get_quiz_id(message)

    if not QuizManager.is_valid(test_id) or not QuizManager.is_author(message.chat.id, test_id):
        await message.answer(get_config_text('telegram', 'question_error_remove'))
        return

    await message.answer(QuizManager.view_quiz(test_id))
