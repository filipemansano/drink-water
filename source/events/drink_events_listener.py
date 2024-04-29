from source.enum.drink_event_enum import DrinkEventEnum
from source.enum.meta_event_enum import MetaEventEnum
from source.enum.person_event_enum import PersonEventEnum
from source.services.drink_service import DrinkService

class DrinkEventListener:
    def __init__(self, service: DrinkService):
        self.service = service

    def register_listeners(self):
        self.service.event_manager.subscribe(DrinkEventEnum.drink_created, self.service.update_meta_history)
        self.service.event_manager.subscribe(MetaEventEnum.meta_updated, self.service.inactive_meta_history)
        self.service.event_manager.subscribe(MetaEventEnum.meta_deleted, self.service.inactive_meta_history)
        self.service.event_manager.subscribe(PersonEventEnum.person_deleted, self.service.remove_drink)