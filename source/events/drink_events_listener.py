from source.enum.drink_event_enum import DrinkEventEnum
from source.services.drink_service import DrinkService

class DrinkEventListener:
    def __init__(self, service: DrinkService):
        self.service = service

    def register_listeners(self):
        self.service.event_manager.subscribe(DrinkEventEnum.drink_created, self.service.update_meta)