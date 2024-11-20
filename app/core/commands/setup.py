from typing import Dict
from aiogram import Router, F

from app.core.modules.hook import Hook
from app.core.modules.quiz_player import QuizPlayer
from app.core.modules.util import *
from app.database.db import *

router = Router()

db = QuizDatabaseManager()


@router.message(F.text == "😎 Начать")
async def first_start(message: types.Message):
    quiz_player = QuizPlayer.get_instance(message.chat.id)

    if quiz_player:
        question_data = quiz_player.get_next_question()
        if question_data:
            await message.answer(get_config_text('telegram', 'test_start'))
            await display_question(message, question_data)
        else:
            await message.answer(get_config_text('telegram', 'test_dont_install'))
    else:
        await message.answer(get_config_text('telegram', 'test_dont_initial'))


@router.message()
async def quiz_answer(message: types.Message):
    quiz_player = QuizPlayer.get_instance(message.chat.id)
    quiz_tracker = QuizTracker.get_instance(str(message.chat.id))

    if not quiz_player:
        return

    question_number = quiz_player.get_question_number()
    quiz_tracker.end_question(question_number, message.text)

    quiz_player.process_answer(message.text)
    question_data = quiz_player.get_next_question()
    if question_data:
        await display_question(message, question_data)
    elif not quiz_tracker.check_test_ended():
        quiz_tracker.end_test()
        quiz_tracker.set_max_score_and_score_player(str(quiz_player.get_max_score()), str(quiz_player.get_score()))
        await message.answer(get_config_text('telegram', 'test_success'), reply_markup=types.ReplyKeyboardRemove())

        Hook.call("test_success", quiz_tracker)
        await db.save_instances_to_database(quiz_tracker)
        author_test_id = QuizManager.get_author_test(quiz_tracker.get_quiz_id())
        await message.bot.send_message(author_test_id, get_config_text('telegram', 'test_success_author')
                                       + " "
                                       + quiz_tracker.get_quiz_id()
                                       + " / "
                                       + str(message.chat.id))

        quiz_tracker.initialize_gpt_psycho_result()
        quiz_tracker.initialize_gpt_about_result()
        Hook.call("test_success_gpt", quiz_tracker)
        await message.bot.send_message(author_test_id, get_config_text('telegram', 'test_success_author_gpt')
                                       + " "
                                       + quiz_tracker.get_quiz_id()
                                       + " / "
                                       + str(message.chat.id))
        await db.save_instances_to_database(quiz_tracker)


async def display_question(message: types.Message, data: Dict[str, str]):
    keyboard = setup_keyboard_questions(data)
    quiz_player = QuizPlayer.get_instance(message.chat.id)
    quiz_tracker = QuizTracker.get_instance(str(message.chat.id))

    if quiz_player:
        quiz_player.set_current_question_data(data)
        question_number = quiz_player.get_question_number()
        quiz_tracker.start_question(question_number, data['question'])

        if not is_keyboard_empty(keyboard):
            await message.answer(data['question'], reply_markup=types.ReplyKeyboardMarkup(
                keyboard=keyboard,
                resize_keyboard=True))
        else:
            await message.answer(data['question'], reply_markup=types.ReplyKeyboardRemove())
