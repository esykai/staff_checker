import shlex

from aiogram import Router
from aiogram.filters.command import Command

from app.core.modules.util import *
from app.database.db import QuizDatabaseManager

router = Router()

db = QuizDatabaseManager()


@router.message(Command(commands=["delete", "del"]))
async def create_question(message: types.Message):
    command, question_number = shlex.split(message.text)

    success = QuizManager.delete_question(message.chat.id, question_number)

    if not success:
        await message.answer(get_config_text('telegram', 'question_error'))
        return

    await message.answer(get_config_text('telegram', 'question_remove'))
    await db.save_quizzes_to_database()
