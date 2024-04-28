from source.events.event_manager import EventManager

class SQSEventAdapter(EventManager):
    def __init__(self, host):
        self.host = host

    def publish(self, topic, message):
        raise NotImplementedError("SQS Event Adapter not implemented")

    def subscribe(self, topic, callback):
        raise NotImplementedError("SQS Event Adapter not implemented")