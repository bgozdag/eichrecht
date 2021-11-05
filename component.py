from abc import ABC, abstractmethod

class Component(ABC):

    @abstractmethod
    def notify(self, message):
        pass

    @abstractmethod
    def receive(self, message):
        pass
