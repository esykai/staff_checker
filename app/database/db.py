import motor.motor_asyncio

from app.core.decorators.singleton import singleton
from app.core.modules.config import get_config_text
from app.core.modules.quiz_manager import QuizManager
from app.core.modules.quiz_tracker import QuizTracker


@singleton
class QuizDatabaseManager:
    __slots__ = ('client', 'db')

    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(get_config_text('database', 'url'))
        self.db = self.client[get_config_text('database', 'collection_name')]

    async def save_quizzes_to_database(self):
        for key, value in QuizManager.quizzes.items():
            await self.save_to_database('quizzes', {'_id': key}, {"$set": value})

    async def save_quiz_id_to_database(self):
        for key, value in QuizManager.quiz_id.items():
            await self.save_to_database('quiz_id', {'_id': key}, {"$set": {'value': value}})

    async def save_instances_to_database(self, object_quiz_tracker: QuizTracker):
        value_json = {slot: getattr(object_quiz_tracker, slot, None) for slot in object_quiz_tracker.__slots__}
        _id = f"{object_quiz_tracker.get_author_id()}" \
              f"/{object_quiz_tracker.get_start_test()}" \
              f"/{object_quiz_tracker.get_end_test()}"

        await self.save_to_database('quiz_history', {'_id': _id}, {"$set": value_json})

        value_json['_id'] = _id
        QuizTracker.from_db(value_json)

    async def save_to_database(self, name, key, data):
        await self.db[name].update_one(key, data, upsert=True)

    async def load_quizzes_from_database(self):
        async for doc in self.db['quizzes'].find():
            quiz_id = doc['_id']
            del doc['_id']
            QuizManager.quizzes[quiz_id] = doc

    async def load_quiz_ids_from_database(self):
        async for doc in self.db['quiz_id'].find():
            quiz_id = doc['_id']
            del doc['_id']
            QuizManager.quiz_id[int(quiz_id)] = doc

    async def load_quiz_history_from_database(self):
        async for doc in self.db["quiz_history"].find():
            QuizTracker.from_db(doc)
