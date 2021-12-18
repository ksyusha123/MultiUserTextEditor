from queue import Queue


class Client:
    def __init__(self):  # сюда бы еще передавать адрес сервера
        self.sent = Queue()
        self.waiting = Queue()

    def put_operation_in_waiting(self, operation):
        self.waiting.put(operation)

    def send_operation(self):
        operation = self.waiting.get()
        # отправить на сервер

    def receive(self):
        pass #todo
