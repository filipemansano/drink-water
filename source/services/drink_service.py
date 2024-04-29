from datetime import datetime, timedelta
from typing import Optional, Union
from source.enum.drink_event_enum import DrinkEventEnum
from source.enum.meta_period_enum import MetaPeriodEnum
from source.events.event_manager import EventManager
from source.model.drink_model import Drink
from source.model.meta_history_model import MetaHistory
from source.model.meta_model import Meta
from source.repository.abstract.drink_repository import IDrinkRepository
from source.repository.abstract.person_repository import IPersonRepository

class DrinkService:
    def __init__(self, repository: IDrinkRepository, person_repository: IPersonRepository, event_manager: EventManager):
        self.repository = repository
        self.person_repository = person_repository
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
    
    def remove_drink(self, person_id: str, drink_id: Optional[str] = None) -> None:
        self.repository.remove_drink(person_id, drink_id)

    
    def inactive_meta_history(self, meta: Union[str, Meta]):
        id = meta if isinstance(meta, str) else meta.id
        self.repository.inactive_meta_history(id)

    def update_meta_history(self, drink: Drink):
        metas = self.person_repository.get_metas(drink.person_id)

        for meta in metas:
            if meta.period == MetaPeriodEnum.daily:
                start = drink.drinked_at.replace(hour=0, minute=0, second=0, microsecond=0)
                end = drink.drinked_at.replace(hour=23, minute=59, second=59, microsecond=999999)
            elif meta.period == MetaPeriodEnum.weekly:
                day_of_week = drink.drinked_at.weekday()

                start = drink.drinked_at - timedelta(days=day_of_week)
                start = start.replace(hour=0, minute=0, second=0, microsecond=0)

                end = start + timedelta(days=6)
                end = end.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            meta = MetaHistory(
                details=meta, 
                person_id=drink.person_id, 
                start_at=start, 
                end_at=end,
                achieved=False)
            
            self.repository.update_meta_history(meta, drink)
            
