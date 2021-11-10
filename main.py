from application import Application
from mediator import Mediator
from message_controller import MessageController

if __name__ == "__main__":
    mediator = Mediator()
    app = Application(mediator)
    message_controller = MessageController(mediator)
    mediator.add(app)
    mediator.add(message_controller)

    message_controller.listen()
    app.run()
