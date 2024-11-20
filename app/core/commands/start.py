from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters.command import Command

from app.core.modules.quiz_player import QuizPlayer
from app.core.modules.quiz_tracker import QuizTracker
from app.core.modules.util import *

router = Router()


@router.message(Command(commands=["start", "play"]))
async def cmd_start(message: types.Message):
    start_status = has_and_valid_quiz_id(message)

    if start_status == StartStatus.right:
        test_id = get_quiz_id(message)
        QuizPlayer(message.chat.id, test_id)
        QuizTracker(str(message.chat.id), test_id)

        keyboard = initialize_keyboard()
        await message.answer(get_config_text('telegram', 'welcome_message_go'),
                             parse_mode=ParseMode.MARKDOWN,
                             reply_markup=keyboard)
    elif start_status == StartStatus.bad_code:
        await message.answer(get_config_text('telegram', 'welcome_message_bad_code'), parse_mode=ParseMode.MARKDOWN)
    elif start_status == StartStatus.nothing:
        await message.answer_sticker(sticker=get_config_text('telegram', 'hey_sticker'))
        await message.answer(get_config_text('telegram', 'welcome_message_no_go'), parse_mode=ParseMode.MARKDOWN)
