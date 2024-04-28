from abc import ABC, abstractmethod

class EventManager(ABC):
    @abstractmethod
    def publish(self, topic, message):
        pass

    @abstractmethod
    def subscribe(self, topic, callback):
        pass