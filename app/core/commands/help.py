from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters.command import Command

from app.core.modules.util import *

router = Router()


@router.message(Command("help"))
async def cmd_start(message: types.Message):
    await message.answer(get_config_text('telegram', 'help_message'), parse_mode=ParseMode.MARKDOWN)
