import socket
from queue import Queue
from client.operations import *

server_address = ("localhost", 5000)


class Client:
    def __init__(self):
        self.sent = Queue()
        self.waiting = Queue()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def put_operation_in_waiting(self, operation):
        self.waiting.put(operation)

    def send_operation(self):
        operation = self.waiting.get()
        # отправить на сервер

    def receive(self):
        pass  # todo

    def create_server(self, file: str):
        operation = CreateServerOperation(file)
        cl = self

        def create_server_function():
            # make async
            cl.sock.connect(server_address)
            cl.sock.sendall(operation.to_json())
        return create_server_function
