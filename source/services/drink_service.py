from datetime import datetime
from typing import Optional
from source.enum.drink_event_enum import DrinkEventEnum
from source.events.event_manager import EventManager
from source.model.drink_model import Drink
from source.repository.drink_repository import IDrinkRepository

class DrinkService:
    def __init__(self, repository: IDrinkRepository, event_manager: EventManager):
        self.repository = repository
        self.event_manager = event_manager
    
    def create_drink(
            self,
            person_id: str,
            ml: float,
            drinked_at: Optional[datetime] = None) -> Drink:
        if not drinked_at:
            drinked_at = datetime.now()
        drink = Drink(ml=ml, person_id=person_id, drinked_at=drinked_at)
        
        drink_created = self.repository.create_drink(drink)
        self.event_manager.publish(DrinkEventEnum.drink_created, drink_created)

        return drink_created
    
    def remove_drink(self, person_id: str, drink_id: str) -> None:
        self.repository.remove_drink(person_id, drink_id)
    
    def update_meta(self, drink: Drink):
        print(f'Updating meta for drink {drink.id}')