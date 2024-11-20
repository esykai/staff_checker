import shlex

from aiogram import Router
from aiogram.filters.command import Command

from app.core.modules.util import *
from app.database.db import QuizDatabaseManager

router = Router()

db = QuizDatabaseManager()

@router.message(Command("gpt"))
async def create_gpt_question(message: types.Message):
    command, question_number, question, gpt_question, *_ = shlex.split(message.text)

    success = QuizManager.create_question_name(message.chat.id, question_number, question)

    if not success:
        await message.answer(get_config_text('telegram', 'question_error'))
        return

    QuizManager.create_question_gpt(message.chat.id, question_number, gpt_question)

    await message.answer(get_config_text('telegram', 'question_add'))
    await db.save_quizzes_to_database()
