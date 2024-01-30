import json
import random
from datetime import datetime

class Event:
    id_counter = 1

    def __init__(self):
        self.id = Event.id_counter
        self.timestamp = datetime.now().isoformat()
        self.metricId = random.randint(1, 10)
        self.metricValue = random.randint(1, 100)
        self.message = f"I created at {self.timestamp}"
        Event.id_counter += 1

    def to_json(self):
        return json.dumps(self.__dict__)
