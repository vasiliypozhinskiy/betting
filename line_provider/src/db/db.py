from abc import ABC, abstractmethod


class AbstractDB(ABC):

    @abstractmethod
    def get_event_by_id(self, id_):
        pass

    @abstractmethod
    def get_all_events(self):
        pass

    @abstractmethod
    def insert_event(self, event):
        pass

    @abstractmethod
    def update_event(self, id_, event):
        pass


db: AbstractDB


def get_db() -> AbstractDB:
    return db
