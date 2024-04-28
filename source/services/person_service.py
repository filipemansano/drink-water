from datetime import datetime
from typing import Optional

from source.model.meta_model import Meta
from source.model.person_model import Person
from source.model.validators.base_validator import init_context
from source.repository.person_repository import IPersonRepository

class PersonService:
    def __init__(self, repository: IPersonRepository):
        self.repository = repository
    
    def get_person(self, person_id: str) -> Person:
        return self.repository.find_person(person_id)
    
    def create_person(
            self, 
            name: str, age: int, 
            weight: float, gender: int) -> Person:
        
        with init_context({'mode': 'create'}):
            person = Person(name=name, age=age, weight=weight, gender=gender)

        person.created_at = datetime.now()
        return self.repository.add_person(person)
    
    def update_person(
            self, 
            person_id: str,
            name: Optional[str] = None, age: Optional[int] = None, 
            weight: Optional[float] = None, gender: Optional[int] = None) -> None:
       
        with init_context({'mode': 'update'}):
            person = Person(id=person_id, name=name, age=age, weight=weight, gender=gender)

        self.repository.update_person(person)
    
    def delete_person(self, person_id: str) -> None:
        self.repository.delete_person(person_id)
    
    def add_meta(self, person_id: str, quantity: float, period: int) -> Meta:
        with init_context({'mode': 'create'}):
            meta = Meta(quantity=quantity, period=period)
        return self.repository.add_meta(person_id, meta)

    def update_meta(self, person_id: str, meta_id: str, quantity: float = None, period: int = None) -> Meta:
        with init_context({'mode': 'update'}):
            meta = Meta(id=meta_id, quantity=quantity, period=period)
        return self.repository.update_meta(person_id, meta)
    
    def remove_meta(self, person_id: str, meta_id: str) -> None:
        self.repository.remove_meta(person_id, meta_id)