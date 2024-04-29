from source.events.adapters.local_event_adapter import LocalEventAdapter
from source.events.adapters.sqs_event_adapter import SQSEventAdapter
from source.config.settings import load_config

config = load_config()

adapter_type = config['messaging']['adapter']

class MessagingFactory:
    def __init__(self):
        self.adapter_type = config['messaging']['adapter']
        
    def get_adapter(self):
        if self.adapter_type == 'local':
            return LocalEventAdapter()
        if self.adapter_type == 'sqs':
            return SQSEventAdapter(host=config['messaging']['host'])
        else:
            raise ValueError("Unsupported adapter type")