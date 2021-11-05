from component import Component

class MessageController(Component):
    def __init__(self, mediator) -> None:
        self._mediator = mediator

    def notify(self, message):
        self._mediator.notify(message, self)

    def receive(self, message):
        print("{} received: {}".format(__class__.__name__, message))