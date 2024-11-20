import enum


class AnswerStatus(enum.Enum):
    not_answer = -1,
    not_right = 0,
    right = 1,
