from typing import Dict, Optional

from app.core.modules.answer_status import AnswerStatus
from app.core.modules.quiz_manager import QuizManager
from app.core.modules.quiz_tracker import QuizTracker


class QuizPlayer:
    """
    Класс QuizPlayer представляет кандидата, проходящего тест.
    """
    instances: Dict[int, 'QuizPlayer'] = {}

    __slots__ = (
        'author_id', 'quiz_id', 'current_question_number', 'correct_answer',
        'points_for_question', 'score', 'max_score'
    )

    def __init__(self, chat_id: int, quiz_id: str):
        self.author_id: int = chat_id
        self.quiz_id: str = quiz_id

        self.current_question_number: int = 1
        self.correct_answer: Optional[str] = None
        self.points_for_question: int = 0
        self.score: int = 0
        self.max_score: int = 0

        # Сохраняем объект QuizPlayer в классовое хранилище
        QuizPlayer.instances[chat_id] = self

    @classmethod
    def get_instance(cls, chat_id: int) -> Optional['QuizPlayer']:
        """
        Возвращает экземпляр QuizPlayer для указанного chat_id.
        """
        return cls.instances.get(chat_id)

    def get_next_question(self) -> Optional[Dict[str, str]]:
        """
        Возвращает данные следующего вопроса. Если вопрос существует, обновляет текущие данные.
        """
        question_data = QuizManager.get_question(self.quiz_id, str(self.current_question_number))
        if question_data:
            self.set_current_question_data(question_data)
            self.current_question_number += 1

        return question_data

    def set_current_question_data(self, question_data: Dict[str, str]) -> None:
        """
        Устанавливает данные текущего вопроса.
        """
        self.correct_answer = question_data.get('correct_answer', "")
        self.points_for_question = int(question_data.get('points', 0))

    def process_answer(self, user_answer: str) -> None:
        """
        Обрабатывает ответ пользователя и обновляет счет.
        """
        quiz_tracker = QuizTracker.get_instance(str(self.author_id))
        if quiz_tracker:
            # Устанавливаем статус ответа на текущий вопрос
            quiz_tracker.set_success_answer(self.get_question_number(), AnswerStatus.not_answer.value)

            if user_answer == self.correct_answer:
                self.score += self.points_for_question
                quiz_tracker.set_success_answer(self.get_question_number(), AnswerStatus.right.value)
            elif self.correct_answer:
                quiz_tracker.set_success_answer(self.get_question_number(), AnswerStatus.not_right.value)

            self.max_score += self.points_for_question

        # Очистка данных о правильном ответе и очках для следующего вопроса
        self.reset_question_data()

    def reset_question_data(self) -> None:
        """
        Сбрасывает данные о правильном ответе и очках после обработки вопроса.
        """
        self.correct_answer = None
        self.points_for_question = 0

    def get_score(self) -> int:
        """
        Возвращает текущий счет игрока.
        """
        return self.score

    def get_question_number(self) -> int:
        """
        Возвращает номер текущего вопроса.
        """
        return self.current_question_number

    def get_max_score(self) -> int:
        """
        Возвращает максимальный возможный счет игрока.
        """
        return self.max_score
