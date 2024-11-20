import shlex

from aiogram import Router
from aiogram.filters.command import Command

from app.core.modules.util import *
from app.database.db import QuizDatabaseManager

router = Router()

db = QuizDatabaseManager()


@router.message(Command(commands=["create", "add"]))
async def create_question(message: types.Message):
    default_values = ["", "", "0"]
    command, question_number, question, options, correct_answer, points, *_ = shlex.split(message.text) + default_values

    success = QuizManager.create_question_name(message.chat.id, question_number, question)

    if not success:
        await message.answer(get_config_text('telegram', 'question_error'))
        return

    if correct_answer != "":
        correct_answer = get_value_by_symbol(options, correct_answer)
        QuizManager.create_question_correct_answer(message.chat.id, question_number, correct_answer)

    if options != "":
        QuizManager.create_question_options(message.chat.id, question_number, options)

    if options != "0":
        QuizManager.create_question_points(message.chat.id, question_number, points)

    await message.answer(get_config_text('telegram', 'question_add'))
    await db.save_quizzes_to_database()
