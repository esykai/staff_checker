from datetime import datetime

from aiogram import Router
from aiogram.filters.command import Command

from app.core.modules.quiz_tracker import QuizTracker
from app.core.modules.util import *


router = Router()


@router.message(Command("get"))
async def get(message: types.Message):
    test_id = get_quiz_id(message)

    if not QuizManager.is_valid(test_id) or not QuizManager.is_author(message.chat.id, test_id):
        await message.answer(get_config_text('telegram', 'get_error'))
        return

    is_empty = True
    for key, value in QuizTracker.instances.items():
        if value.get_quiz_id() != test_id or not value.check_test_ended() or not is_history(key):
            continue

        is_empty = False
        result = ""
        result += "**********************\n"
        result += f"👩🏼‍💻 ID: {value.get_author_id()}\n\n"

        result += f"⌛️ Дата начала: {datetime.fromtimestamp(value.get_start_test())}\n"
        result += f"⌛️ Дата окончания: {datetime.fromtimestamp(value.get_end_test())}\n\n"
        result += f"{value.get_gpt_about()}\n\n"

        for question_number, answer in value.get_user_answers().items():
            status = get_answer_status_symbol(answer['success'])
            result += f"💻 {value.get_question_text(question_number)}: "
            result += f"{status} Ответ - {answer['answer']}, "
            result += f"Время - {round(value.get_question_duration(question_number), 2)} сек.\n\n"

        result += f"\n🖥 Score: {value.get_max_score_and_score_player()}\n"
        result += f"🖥 Отзыв GPT: {value.get_gpt_psycho()}\n"
        result += "**********************"

        for chunk in split_into_chunks(result, chunk_size=4096):  # NOTE: телеграм имеет ограничение 4096 символов
            await message.answer(chunk)

    if is_empty:
        await message.answer(get_config_text('telegram', 'get_empty'))
