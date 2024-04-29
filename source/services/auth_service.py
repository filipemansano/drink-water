from source.model.person_model import Person
from source.repository.person_repository import IPersonRepository
from source.services.helpers import chipper_password

class AuthService:
    def __init__(self, person_repository: IPersonRepository):
        self.person_repository = person_repository
    
    def authenticate(self, email: str, password: str) -> Person:
        person = self.person_repository.find_person_by_email(email)
        if not person:
            return False
        
        if person.password.get_secret_value() != chipper_password(password):
            return False
        
        return person
    