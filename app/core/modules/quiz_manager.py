from typing import Dict, Optional, Any


class QuizManager:
    """
    Класс для управления процессом проведения тестов.
    Хранит данные о тестах и позволяет добавлять вопросы, удалять их, а также настраивать варианты ответов и правильные ответы.

    Данные сохраняются в словарях:
    - quizzes: Хранит информацию о тестах.
    - quiz_id: Хранит соответствие chat_id и quiz_code.
    """

    quizzes: Dict[str, Dict[Any, Any]] = {}
    quiz_id: Dict[int, str] = {}

    @classmethod
    def initialize_quiz(cls, chat_id: int, code: str) -> str:
        """
        Инициализирует новый тест, если он еще не существует.
        Сохраняет связь между chat_id и кодом теста.

        :param chat_id: ID чата, который создает тест.
        :param code: Уникальный код теста.
        :return: Код теста.
        """
        if code not in cls.quizzes:
            cls.quizzes[code] = {'author_id': chat_id}
        cls.quiz_id[chat_id] = code
        return code

    @classmethod
    def is_valid(cls, quiz_id: str) -> bool:
        """
        Проверяет, существует ли тест с данным кодом.

        :param quiz_id: Код теста.
        :return: True, если тест существует, иначе False.
        """
        return quiz_id in cls.quizzes

    @classmethod
    def check_can_create_question(cls, chat_id: int) -> bool:
        """
        Проверяет, может ли пользователь создавать вопросы для теста.

        :param chat_id: ID чата пользователя.
        :return: True, если пользователь может создавать вопросы, иначе False.
        """
        return chat_id in cls.quiz_id

    @classmethod
    def create_question_name(cls, chat_id: int, question_number: str, question: str) -> bool:
        """
        Создает вопрос с заданным номером и текстом.

        :param chat_id: ID чата пользователя.
        :param question_number: Номер вопроса.
        :param question: Текст вопроса.
        :return: True, если вопрос был успешно создан, иначе False.
        """
        if not cls.check_can_create_question(chat_id):
            return False

        cls.quizzes[cls.quiz_id[chat_id]][question_number] = {'question': question}
        return True

    @classmethod
    def delete_question(cls, chat_id: int, question_number: str) -> bool:
        """
        Удаляет вопрос из теста.

        :param chat_id: ID чата пользователя.
        :param question_number: Номер вопроса для удаления.
        :return: True, если вопрос был успешно удален, иначе False.
        """
        if not cls.check_can_create_question(chat_id):
            return False

        quiz_id = cls.quiz_id.get(chat_id)
        if quiz_id is None:
            return False

        if question_number not in cls.quizzes[quiz_id]:
            return False

        del cls.quizzes[quiz_id][question_number]
        cls.reindex_questions(quiz_id)

        return True

    @classmethod
    def create_question_options(cls, chat_id: int, question_number: str, options: str) -> bool:
        """
        Добавляет варианты ответов для вопроса.

        :param chat_id: ID чата пользователя.
        :param question_number: Номер вопроса.
        :param options: Варианты ответов.
        :return: True, если опции были добавлены, иначе False.
        """
        if not cls.check_can_create_question(chat_id):
            return False

        cls.quizzes[cls.quiz_id[chat_id]][question_number]['options'] = options
        return True

    @classmethod
    def create_question_correct_answer(cls, chat_id: int, question_number: str, correct_answer: str) -> bool:
        """
        Устанавливает правильный ответ для вопроса.

        :param chat_id: ID чата пользователя.
        :param question_number: Номер вопроса.
        :param correct_answer: Правильный ответ.
        :return: True, если правильный ответ был установлен, иначе False.
        """
        if not cls.check_can_create_question(chat_id):
            return False

        cls.quizzes[cls.quiz_id[chat_id]][question_number]['correct_answer'] = correct_answer
        return True

    @classmethod
    def create_question_points(cls, chat_id: int, question_number: str, points: str) -> bool:
        """
        Устанавливает количество баллов за вопрос.

        :param chat_id: ID чата пользователя.
        :param question_number: Номер вопроса.
        :param points: Количество баллов.
        :return: True, если баллы были установлены, иначе False.
        """
        if not cls.check_can_create_question(chat_id):
            return False

        cls.quizzes[cls.quiz_id[chat_id]][question_number]['points'] = points
        return True

    @classmethod
    def create_question_gpt(cls, chat_id: int, question_number: str, gpt: str) -> bool:
        """
        Добавляет информацию о GPT для вопроса.

        :param chat_id: ID чата пользователя.
        :param question_number: Номер вопроса.
        :param gpt: Информация о GPT.
        :return: True, если информация была добавлена, иначе False.
        """
        if not cls.check_can_create_question(chat_id):
            return False

        cls.quizzes[cls.quiz_id[chat_id]][question_number]['gpt'] = gpt
        return True

    @classmethod
    def get_question(cls, quiz_id: str, question_number: str) -> Optional[Dict[str, str]]:
        """
        Получает информацию о вопросе по его номеру.

        :param quiz_id: Код теста.
        :param question_number: Номер вопроса.
        :return: Словарь с данными вопроса или None, если вопрос не найден.
        """
        return cls.quizzes.get(quiz_id, {}).get(question_number)

    @classmethod
    def get_author_test(cls, test_id: str) -> int:
        """
        Получает ID автора теста.

        :param test_id: Код теста.
        :return: ID автора теста.
        """
        return cls.quizzes[test_id]['author_id']

    @classmethod
    def is_author(cls, chat_id: int, test_id: str) -> bool:
        """
        Проверяет, является ли пользователь автором теста.

        :param chat_id: ID чата пользователя.
        :param test_id: Код теста.
        :return: True, если пользователь является автором, иначе False.
        """
        return cls.quizzes.get(test_id, {}).get('author_id') == chat_id

    @classmethod
    def view_quiz(cls, test_id: str) -> str:
        """
        Формирует и возвращает строковое представление всего теста с вопросами.

        :param test_id: Код теста.
        :return: Строка с информацией о тесте.
        """
        quiz = cls.quizzes.get(test_id)
        if not quiz:
            return ""

        quiz_info = ""
        for question_number, question_data in quiz.items():
            if question_number == "author_id":
                continue

            if question_data:
                quiz_info += f"❓ Вопрос {question_number}: {question_data['question']}\n"
                quiz_info += f"  🔹 Опции: {question_data.get('options')}\n"
                quiz_info += f"  ⭐️ Поинты: {question_data.get('points')}\n"
                quiz_info += f"  💡 GPT: {question_data.get('gpt')}\n"
                quiz_info += f"  ✔️ Правильный ответ: {question_data.get('correct_answer')}\n\n"

        return quiz_info

    @classmethod
    def reindex_questions(cls, quiz_id: str):
        """
        Перенумеровывает вопросы в тесте, чтобы их номера шли последовательно.

        :param quiz_id: Код теста.
        """
        updated_questions = {}
        new_question_number = 1
        for question_num, question_data in cls.quizzes[quiz_id].items():
            if question_num == "author_id":
                updated_questions['author_id'] = question_data
                continue

            if question_data is None:
                continue

            updated_questions[str(new_question_number)] = question_data
            new_question_number += 1

        cls.quizzes[quiz_id] = updated_questions
