from aiogram import Router
from aiogram.filters.command import Command

from app.core.modules.util import *
from app.database.db import QuizDatabaseManager

router = Router()

db = QuizDatabaseManager()


@router.message(Command(commands=["initialize", "init"]))
async def initialize(message: types.Message):
    test_id = get_quiz_id(message)
    is_valid_quiz = QuizManager.is_valid(test_id)
    is_author = QuizManager.is_author(message.chat.id, test_id)

    if not is_valid_quiz or is_author:
        QuizManager.initialize_quiz(message.chat.id, test_id)
        await message.answer(get_config_text('telegram', 'ident_success'))
        await db.save_quiz_id_to_database()
    else:
        await message.answer(get_config_text('telegram', 'ident_error'))
