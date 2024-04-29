from source.config.settings import load_config
from source.repository.abstract.drink_repository import IDrinkRepository
from source.repository.mongodb.drink_repository import MongoDBDrinkRepository
from source.repository.mongodb.person_repository import MongoDBPersonRepository
from source.repository.abstract.person_repository import IPersonRepository

config = load_config()

class RepositoryFactory:

    def __init__(self):
        self.repository_type = config['repository']['type']
        self.repository_map = {
            'mongodb': {
                IDrinkRepository: MongoDBDrinkRepository,
                IPersonRepository: MongoDBPersonRepository,
            }
        }

    def get_repository(self, interface):
        repo_map = self.repository_map.get(self.repository_type)
        if repo_map is None:
            raise ValueError(f"Unsupported repository type: {self.repository_type}")
        repository_class = repo_map.get(interface)
        if repository_class is None:
            raise ValueError(f"No repository found for interface {interface}")
        return repository_class()