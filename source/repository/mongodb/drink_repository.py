
from bson import ObjectId
from source.database.mongodb_connection import MongoDBConnection
from source.model.drink_model import Drink
from source.repository.drink_repository import IDrinkRepository

class MongoDBDrinkRepository(IDrinkRepository):
    def __init__(self):
        db_connection = MongoDBConnection()
        client = db_connection.get_client()
        db = client['drink_db']
        self.collection = db['drink']

    def create_drink(self, drink: Drink) -> Drink:
        data_to_insert = drink.model_dump(exclude=['id'], exclude_none=True)
        data_to_insert['person_id'] = ObjectId(data_to_insert['person_id'])

        drink_data = self.collection.insert_one(data_to_insert)

        drink.id = str(drink_data.inserted_id)
        return drink

    def remove_drink(self, person_id: str, drink_id) -> None:
        self.collection.delete_one({'person_id': ObjectId(person_id), '_id': ObjectId(drink_id)})