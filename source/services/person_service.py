from datetime import datetime
from typing import Optional
from source.enum.meta_event_enum import MetaEventEnum
from source.enum.person_event_enum import PersonEventEnum
from source.events.event_manager import EventManager
from source.model.meta_model import Meta
from source.model.person_model import Person
from source.model.validators.base_validator import init_context
from source.repository.person_repository import IPersonRepository
from source.services.helpers import chipper_password

class PersonService:
    def __init__(self, repository: IPersonRepository, event_manager: EventManager):
        self.repository = repository
        self.event_manager = event_manager
    
    def get_person(self, person_id: str) -> Person:
        return self.repository.find_person(person_id)
    
    def get_metas(self, person_id: str) -> Person:
        return self.repository.get_metas(person_id)
    
    def create_person(
            self, 
            name: str, age: int, 
            weight: float, gender: int, password: str, email: str) -> Person:
        
        with init_context({'mode': 'create'}):
            person = Person(name=name, age=age, weight=weight, gender=gender, email=email, password=chipper_password(password))

        if self.repository.find_person_by_email(email):
            raise ValueError('Email already exists')
        
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
        self.event_manager.publish(PersonEventEnum.person_deleted, person_id)
    
    def add_meta(self, person_id: str, quantity: float, period: int) -> Meta:
        with init_context({'mode': 'create'}):
            meta = Meta(quantity=quantity, period=period)
        return self.repository.add_meta(person_id, meta)

    def update_meta(self, person_id: str, meta_id: str, quantity: float = None, period: int = None) -> Meta:
        with init_context({'mode': 'update'}):
            meta = Meta(id=meta_id, quantity=quantity, period=period)
        meta = self.repository.update_meta(person_id, meta)
        self.event_manager.publish(MetaEventEnum.meta_updated, meta_id)
        return meta
    
    def remove_meta(self, person_id: str, meta_id: str) -> None:
        self.repository.remove_meta(person_id, meta_id)
        self.event_manager.publish(MetaEventEnum.meta_deleted, meta_id)