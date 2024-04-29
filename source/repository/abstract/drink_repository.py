from typing import Optional
from source.model.drink_model import Drink
from source.model.meta_history_model import MetaHistory

class IDrinkRepository:
    def create_drink(self, drink: Drink) -> Drink:
        pass

    def remove_drink(self, person_id: str, drink_id: Optional[str] = None) -> None:
        pass
    
    def inactive_meta_history(self, meta_id: str) -> None:
        pass

    def update_meta_history(self, meta: MetaHistory, drink: Drink) -> None:
        pass