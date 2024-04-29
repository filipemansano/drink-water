
from bson import ObjectId
from source.model.person_model import Person
from source.database.mongodb_connection import MongoDBConnection
from source.model.meta_model import Meta
from source.repository.person_repository import IPersonRepository
import uuid

class MongoDBPersonRepository(IPersonRepository):
    def __init__(self):
        db_connection = MongoDBConnection()
        client = db_connection.get_client()
        db = client['drink_db']
        self.collection = db['person']

    def add_person(self, person: Person) -> Person:
        data = person.model_dump(exclude=['id', 'metas'], exclude_none=True)
        data['password'] = person.password.get_secret_value()
        person_data = self.collection.insert_one(data)

        person.id = str(person_data.inserted_id)
        return person

    def update_person(self, person: Person) -> None:
        self.collection.update_one(
            {'_id': ObjectId(person.id)}, 
            {'$set': person.model_dump(exclude=['id', 'metas'], exclude_none=True)}
        )
        return person

    def delete_person(self, person_id: str) -> None:
        self.collection.delete_one({'_id': ObjectId(person_id)})

    def find_person(self, person_id: str) -> Person:
        person_data = self.collection.find_one({'_id': ObjectId(person_id)})
        if person_data:
            person_data['id'] = str(person_data.pop('_id'))
            return Person(**person_data)
        return None

    def find_person_by_email(self, email: str) -> Person:
        person_data = self.collection.find_one({'email': email})
        if person_data:
            person_data['id'] = str(person_data.pop('_id'))
            return Person(**person_data)
        return None

    def add_meta(self, person_id: str, meta: Meta) -> Meta:
        meta.id = str(uuid.uuid4())
        self.collection.update_one(
            {'_id': ObjectId(person_id)}, 
            {'$push': {'meta': meta.model_dump()}}
        )

        return meta

    def get_metas(self, person_id: str) -> list[Meta]:
        person_data = self.collection.find_one({'_id': ObjectId(person_id)}, {'_id': 0, 'meta': 1})
        if person_data:
            metas = [Meta(**meta) for meta in person_data['meta']]
            return metas
        return None
    
    def remove_meta(self, person_id: str, meta_id: str) -> None:
        self.collection.update_one(
            {'_id': ObjectId(person_id)}, 
            {'$pull': {'meta': {'id': meta_id}}}
        )
    
    def update_meta(self, person_id: str, meta: Meta) -> None:
        data = meta.model_dump(exclude='id', exclude_none=True)

        mongodb_fields = {f"meta.$.{key}": value for key, value in data.items()}

        self.collection.update_one(
            {'_id': ObjectId(person_id), 'meta.id': meta.id}, 
            {'$set': mongodb_fields}
        )