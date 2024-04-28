from source.model.drink_model import Drink

class IDrinkRepository:
    def create_drink(self, drink: Drink) -> Drink:
        pass

    def remove_drink(self, person_id: str, drink_id: str) -> None:
        pass