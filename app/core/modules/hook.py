class Hook:
    """
    Класс Hook представляет собой хук, который является аналогом делегатов в Java и C#.

    Хуки позволяют зарегистрировать несколько функций (подписчиков) для прослушивания и реагирования на события.
    Когда событие происходит, хук вызывает все зарегистрированные подписчики последовательно для обработки события.

    Использование:
        Hook.add(event_name, func) - добавляет функцию в качестве подписчика к хуку для указанного события.
        Hook.call(event_name, data) - вызывает все зарегистрированные подписчики для указанного события с
        предоставленными данными события.

    Атрибуты:
        global_hooks (dict): Словарь для хранения зарегистрированных событий и их подписчиков.

    Методы:
        add(event_name, func): Добавляет функцию в качестве подписчика к хуку для указанного события.
        call(event_name, data): Вызывает все зарегистрированные подписчики для указанного события с
        предоставленными данными события.
    """
    global_hooks = {}

    @classmethod
    def add(cls, event_name, func):
        if event_name not in cls.global_hooks:
            cls.global_hooks[event_name] = []
        cls.global_hooks[event_name].append(func)

    @classmethod
    def call(cls, event_name, data):
        if event_name in cls.global_hooks:
            for func in cls.global_hooks[event_name]:
                func(data)
