import uuid

from db.db import AbstractDB
from model.event import Event


class InMemoryDB(AbstractDB):
    events: dict[str, Event] = {}

    def get_event_by_id(self, id_):
        return self.events[id_]

    def get_all_events(self):
        return self.events

    def insert_event(self, event):
        event.id = uuid.uuid4()
        self.events[str(event.id)] = event

    def update_event(self, id_, event):
        self.events[id_] = event
