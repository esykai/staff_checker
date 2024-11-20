import enum


class StartStatus(enum.Enum):
    nothing = -1,
    bad_code = 0,
    right = 1,
