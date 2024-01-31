import json
import random
from datetime import datetime

class Event:
    #Represents an event with a unique ID, timestamp, and random metrics.
    id_counter = 1  # Class variable to keep track of the last assigned ID

    def __init__(self):
        #Initializes a new Event instance with unique details.
        self.reporter_id = Event.id_counter  
        self.timestamp = datetime.now().isoformat() 
        self.metric_id = random.randint(1, 10) 
        self.metric_value = random.randint(1, 100)  
        self.message = f"I was created at {self.timestamp}"  
        Event.id_counter += 1 

    def to_json(self) -> str:
        #Converts the event instance to a JSON string.
        return json.dumps(self.__dict__)
