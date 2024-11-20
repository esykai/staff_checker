from typing import Dict, Optional, Any
from datetime import datetime

from app.core.modules.quiz_manager import QuizManager
from app.core.modules.util import gpt_psycho, get_answer_status_symbol, gpt


class QuizTracker:
    """
    Класс для отслеживания процесса прохождения теста.
    !Отправляется в базу данных: instances
    """
    instances: Dict[str, 'QuizTracker'] = {}

    __slots__ = [
        'author_id', 'quiz_id', 'user_answers', 'question_text', 'question_times',
        'test_success', 'gpt_psycho', 'gpt_about', 'max_score_and_score_player'
    ]

    def __init__(self, user_id: str, quiz_id: str, user_answers=None, question_text=None, question_times=None,
                 test_success: bool = False, gpt_psycho: str = "В процессе...", gpt_about: str = "",
                 max_score_and_score_player: str = ""):
        if '/' in user_id:
            chat_id, _, _ = user_id.split('/')
            self.author_id: str = chat_id
        else:
            self.author_id: str = user_id

        self.quiz_id: str = quiz_id
        self.user_answers: Dict[str, Any] = user_answers or {}
        self.question_text: Dict[str, str] = question_text or {}
        self.question_times: Dict[str, Dict[str, float]] = question_times or {}
        self.test_success: bool = test_success
        self.gpt_psycho: str = gpt_psycho
        self.gpt_about: str = gpt_about
        self.max_score_and_score_player: str = max_score_and_score_player

        QuizTracker.instances[user_id] = self

    @classmethod
    def from_db(cls, db_record: Dict[str, Any]) -> 'QuizTracker':
        return cls(
            user_id=db_record['_id'],
            quiz_id=db_record['quiz_id'],
            user_answers=db_record.get('user_answers'),
            question_text=db_record.get('question_text'),
            question_times=db_record.get('question_times'),
            test_success=db_record.get('test_success', False),
            gpt_psycho=db_record.get('gpt_psycho', "В процессе..."),
            gpt_about=db_record.get('gpt_about', ""),
            max_score_and_score_player=db_record.get('max_score_and_score_player', "")
        )

    @classmethod
    def get_instance(cls, chat_id: str) -> Optional['QuizTracker']:
        return cls.instances.get(chat_id)

    def start_question(self, question_number: int, question_text: str) -> None:
        question_number_str = str(question_number - 1)
        self.user_answers[question_number_str] = {}
        self.question_times[question_number_str] = {'start': datetime.now().timestamp()}
        self.question_text[question_number_str] = question_text

    def end_question(self, question_number: int, user_answer: str) -> None:
        question_number_str = str(question_number - 1)
        self.user_answers[question_number_str]['answer'] = user_answer
        self.question_times[question_number_str]['end'] = datetime.now().timestamp()

    def set_success_answer(self, question_number: int, success_or_not: str) -> None:
        question_number_str = str(question_number - 1)
        self.user_answers[question_number_str]['success'] = success_or_not[0]

    def get_question_duration(self, question_number: str) -> Optional[float]:
        question_time = self.question_times.get(question_number)
        if question_time and 'start' in question_time and 'end' in question_time:
            start = question_time['start']
            end = question_time['end']
            return end - start
        else:
            return None

    def get_question_text(self, question_number: str) -> Optional[str]:
        return self.question_text.get(question_number)

    def end_test(self) -> None:
        self.test_success = True

    def initialize_gpt_psycho_result(self) -> None:
        data_text_for_gpt_psycho = ""

        for question_number, answer in self.get_user_answers().items():
            status = get_answer_status_symbol(answer['success'])
            data_text_for_gpt_psycho += f"💻 {self.get_question_text(question_number)}: "
            data_text_for_gpt_psycho += f"{status} Ответ - {answer['answer']}, "
            data_text_for_gpt_psycho += f"Время - {round(self.get_question_duration(question_number), 2)} сек. | "

        data_text_for_gpt_psycho += f" | score: {self.get_max_score_and_score_player()}"
        self.gpt_psycho = gpt_psycho(data_text_for_gpt_psycho)

    def initialize_gpt_about_result(self) -> None:
        data_text_for_gpt_about = ""

        for question_number, answer in self.get_user_answers().items():
            gpt_request = QuizManager.get_question(self.get_quiz_id(), question_number).get('gpt')

            if gpt_request:
                data_text_for_gpt_about += gpt(f"{gpt_request}: {answer['answer']}")

        self.gpt_about = data_text_for_gpt_about

    def set_max_score_and_score_player(self, max_score: str, score_player: str) -> None:
        self.max_score_and_score_player = f"{score_player} / {max_score}"

    def get_max_score_and_score_player(self) -> str:
        return self.max_score_and_score_player

    def get_gpt_psycho(self) -> str:
        return self.gpt_psycho

    def get_gpt_about(self) -> str:
        return self.gpt_about

    def get_start_test(self) -> float:
        return self.question_times['1']['start']

    def get_end_test(self) -> float:
        return self.question_times[str(len(self.question_text))]['end']

    def get_quiz_id(self) -> str:
        return self.quiz_id

    def get_author_id(self) -> str:
        return self.author_id

    def get_user_answers(self) -> Dict[str, Any]:
        return self.user_answers

    def get_status_answer(self, question_number: int) -> int:
        return self.user_answers.get(str(question_number), {}).get('success', 0)

    def check_test_ended(self) -> bool:
        return self.test_success
