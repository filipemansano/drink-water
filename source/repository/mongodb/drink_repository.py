
from typing import Optional
from bson import ObjectId
from source.database.mongodb_connection import MongoDBConnection
from source.model.drink_model import Drink
from source.model.meta_history_model import MetaHistory
from source.repository.drink_repository import IDrinkRepository

class MongoDBDrinkRepository(IDrinkRepository):
    def __init__(self):
        db_connection = MongoDBConnection()
        client = db_connection.get_client()
        self.db = client['drink_db']
        self.collection = self.db['drink']

    def create_drink(self, drink: Drink) -> Drink:
        data_to_insert = drink.model_dump(exclude=['id'], exclude_none=True)
        data_to_insert['person_id'] = ObjectId(data_to_insert['person_id'])

        drink_data = self.collection.insert_one(data_to_insert)

        drink.id = str(drink_data.inserted_id)
        return drink

    def remove_drink(self, person_id: str, drink_id: Optional[str] = None) -> None:
        filters = {'person_id': ObjectId(person_id)}
        if drink_id:
            filters['id'] = ObjectId(drink_id)
            self.collection.delete_one(filters)
        else:
            self.collection.delete_many(filters)
    
    def inactive_meta_history(self, meta_id: str) -> None:
        self.db['drink_history'].update_one(
            {
                'meta.id': meta_id,
                'inactive': False
            },
            {
                '$set': {
                    'inactive': True
                }
            }
        )

    def update_meta_history(self, meta: MetaHistory, drink: Drink) -> None:
        meta_quantity = meta.details.quantity * (7 if meta.details.period == 'weekly' else 1)
        self.db['drink_history'].update_one(
            {
                'start': meta.start_at, 'end': meta.end_at, 
                'meta.period': meta.details.period, 'meta.quantity': meta_quantity, 'meta.id': meta.details.id,
                'inactive': False
            },
            [
                {
                    '$set': {
                        'ml_dring': {'$add': [drink.ml, {'$ifNull': [ "$ml_dring", 0]}]},
                    }
                },
                {
                    '$set': {
                        'ml_drink_left': {'$subtract': ['$meta.quantity', '$ml_dring']},
                    }
                },
                {
                    '$set': {
                        'achieved': {
                            '$cond': {
                                'if': {'$lte': ['$ml_drink_left', 0]}, 
                                'then': True, 
                                'else': False
                            }
                        }
                    }
                }
            ],
            upsert=True
        )