import json
import socket
import uuid
from queue import Queue
from client.operations import *
from threading import Thread, Lock

server_address = ("localhost", 5000)


class Client:
    def __init__(self):
        self.guid = uuid.uuid1()
        self.waiting = Queue()
        self.waiting_ack = None
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver.bind(('localhost', 63201))
        self.receiver.listen()
        self.connected = False
        self.file_id = None
        self.lock = Lock()

    def put_operation_in_waiting(self, operation):
        self.waiting.put(operation)

    def send(self):
        operation = self.waiting.get()
        # отправить на сервер

    def receive(self):
        while self.connected:
            sock, addr = self.receiver.accept()
            response = self.get_response(sock)
            if response['operation'] == 'ack':
                self.lock.acquire()
                self.waiting_ack = None
                self.lock.release()
            else:
                operation = response['operation']

    def get_response(self, sock):
        data = []
        while True:
            r = sock.recv(1024)
            if not r:
                break
            data.append(r.decode())
        return json.loads(''.join(data))

    def create_server(self, file: str):
        operation = CreateServerOperation(file)
        cl = self

        def create_server_function():
            for i in range(3):
                try:
                    cl.sender.connect(server_address)
                    cl.sender.sendall(operation.to_json())
                except socket.error:
                    continue
                finally:
                    sock, addr = cl.receiver.accept()
                    response = self.get_response(sock)
                    if response['id']:
                        self.file_id = response['id']
                        self.connected = True
                        Thread(target=cl.receive).start()
                        Thread(target=cl.send).start()
                    break

        return Thread(target=create_server_function).start
