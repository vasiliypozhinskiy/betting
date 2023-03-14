from abc import ABC, abstractmethod


class AbstractDB(ABC):

    @abstractmethod
    def get_by_id(self, table, id_):
        pass

    @abstractmethod
    def get_all(self, table):
        pass

    @abstractmethod
    def insert(self, table, entity):
        pass

    @abstractmethod
    def update(self, table, id_, entity):
        pass


db: AbstractDB


def get_db() -> AbstractDB:
    return db
