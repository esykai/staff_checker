# Candidate Quiz Bot 🤖

Этот Telegram-бот разработан для проведения тестирования кандидатов перед собеседованием. Работодатели могут создавать тесты, а кандидаты проходить их, отвечать на вопросы и получать детальную обратную связь. 🚀

---

## ✨ Особенности

- **Инициализация теста**  
  Работодатель может запустить тест, указав уникальный `TEST_ID`.  
- **Создание вопросов**  
  Авторы теста добавляют вопросы, варианты ответов и указывают правильные ответы.  
- **Участие в тестах**  
  Кандидаты присоединяются к тесту и проходят его шаг за шагом.  
- **Оценка**  
  Бот автоматически подсчитывает баллы каждого участника. 📊  
- **Уведомление о завершении**  
  Авторы теста получают уведомление, когда кандидат завершает викторину. 🔔  
- **Интеграция с GPT**  
  Бот анализирует результаты с помощью GPT и предоставляет обратную связь: плюсы и минусы кандидата. 🧠  
- **Оценка времени реакции**  
  Измеряет, сколько времени кандидат тратит на каждый вопрос. ⏱️  

---

## 📸 Пример работы

### Синхронизация с базой данных
- **Инициализация теста:**  
  ![Инициализация теста](https://i.imgur.com/rsB684E.png)  
- **Прохождение теста:**  
  ![Прохождение теста](https://i.imgur.com/Pd6IXL3.png)  

### Уведомление о завершении
  ![Уведомление](https://i.imgur.com/gYvuoPO.png)  

### Анализ GPT
  ![GPT-анализ](https://i.imgur.com/y1e1KmO.png)  

---

## 🛠️ Установка и запуск

1. **Клонируйте репозиторий**  
   ```
   git clone https://github.com/esykai/pet_project_staff_checker.git
   ```

2. **Установите зависимости**  
   ```
   pip install -r requirements.txt
   ```

3. **Запустите бота**  
   ```
   python run.py
   ```

---

## ⚙️ Конфигурация

- Отредактируйте файл `Constants/constants.ini`, чтобы настроить:  
  - Токены API 📡  
  - Параметры базы данных 🗄️  
  - Шаблоны сообщений ✍️  

---

## 🌟 Почему этот бот крутой?

- Удобный интерфейс в Telegram.  
- Автоматизация тестирования кандидатов.  
- Интеллектуальная обратная связь с GPT.  
- Полная кастомизация под ваши нужды!  

Готовы упростить процесс найма? Попробуйте Candidate Quiz Bot уже сегодня! 💼
