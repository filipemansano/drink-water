from typing import List
from source.model.person_model import Person
from source.model.meta_model import Meta

class IPersonRepository:
    def add_person(self, person: Person) -> Person:
        pass

    def update_person(self, person: Person) -> None:
        pass

    def delete_person(self, person_id: str) -> None:
        pass

    def find_person(self, person_id: str) -> Person:
        pass

    def add_meta(self, person_id: str, meta: Meta) -> Meta:
        pass

    def get_metas(self, person_id: str) -> List[Meta]:
        pass

    def remove_meta(self, person_id: str, meta_id: str) -> None:
        pass

    def update_meta(self, person_id: str, meta: Meta) -> None:
        pass