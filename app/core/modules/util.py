import re
import pytgpt.phind as phind

from aiogram import types
from g4f.client import Client

from app.core.modules.answer_status import AnswerStatus
from app.core.modules.config import get_config_text
from app.core.modules.start_status import StartStatus
from app.core.modules.quiz_manager import QuizManager


def has_and_valid_quiz_id(message):
    split_text = message.text.split()
    if len(split_text) > 1:
        if QuizManager.is_valid(split_text[1]):
            return StartStatus.right
        else:
            return StartStatus.bad_code
    else:
        return StartStatus.nothing


def initialize_keyboard():
    kb = [
        [types.KeyboardButton(text="😎 Начать")],
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


def get_quiz_id(message):
    return message.text.split()[1].lower()


def get_value_by_symbol(text, letter):
    if len(letter) == 1:
        letter += ')'

    next_letter_index = ord(letter[0]) + 1
    next_letter = chr(next_letter_index)

    if text.find(next_letter + ")") != -1:
        return text[text.find(letter) + 2:text.find(next_letter + ")")].strip()
    else:
        return text[text.find(letter) + 2:].strip()


def setup_keyboard_questions(data):
    options = data.get('options', "")
    kb = []

    split_text = re.split(r'[а-я]\)', options)
    for part in split_text:
        kb.append([types.KeyboardButton(text=part.strip())])

    return kb


client = Client()


def gpt_psycho(text):
    return gpt(get_config_text('gpt', 'psycho') + text)


def gpt(prompt):
    bot = phind.PHIND()
    bot_response = bot.chat(prompt)

    try:
        return bot_response
    except:
        return ""

def get_answer_status_symbol(status):
    if status == AnswerStatus.right.value[0]:
        return '✅'
    elif status == AnswerStatus.not_right.value[0]:
        return '❌'
    else:
        return '❓'


def split_into_chunks(string, chunk_size):
    for i in range(0, len(string), chunk_size):
        yield string[i:i + chunk_size]


def is_keyboard_empty(keyboard):
    if len(keyboard) == 1:
        return True
    else:
        return False


def is_history(user_id):
    if '/' in user_id:
        return True
    else:
        return False
