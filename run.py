import os
import asyncio
import nest_asyncio

from aiogram import Bot, Dispatcher

from app.core.modules.config import get_config_text
from app.core.commands import get, help, gpt, initialize, delete, start, create, view, setup
from app.database.db import QuizDatabaseManager

API_TOKEN = get_config_text('telegram', 'api_token')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
nest_asyncio.apply()


for file_name in os.listdir("app/core/hooks"):
    if file_name.endswith(".py"):
        module_name = file_name.replace('.py', '')

        try:
            exec(f"import app.core.hooks.{module_name}")
            print(f"Imported module {module_name}")
        except Exception as e:
            print(f"Failed to import module {module_name}: {str(e)}")


async def main():
    database_handler = QuizDatabaseManager()

    await database_handler.load_quizzes_from_database()
    await database_handler.load_quiz_ids_from_database()
    await database_handler.load_quiz_history_from_database()

    await database_handler.save_quizzes_to_database()
    await database_handler.save_quiz_id_to_database()

    dp.include_routers(help.router,
                       start.router,
                       get.router,
                       initialize.router,
                       create.router,
                       delete.router,
                       view.router,
                       gpt.router,
                       setup.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
