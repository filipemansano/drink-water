from source.events.event_manager import EventManager

class LocalEventAdapter(EventManager):
    def __init__(self):
        self.topics = {}

    def publish(self, topic, message):
        if topic in self.topics:
            for callback in self.topics[topic]:
                callback(message)

    def subscribe(self, topic, callback):
        if topic not in self.topics:
            self.topics[topic] = []
        self.topics[topic].append(callback)