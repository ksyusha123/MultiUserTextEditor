import sys
from PyQt5.QtWidgets import QApplication
from gui import TextEditor
import json
import socket
import uuid
from queue import Queue
from common.operations import *
from threading import Thread, Lock

server_address = ("localhost", 5000)


class Client:
    def __init__(self):
        self.guid = uuid.uuid1()
        self.waiting = Queue()
        self.previous_operation = None
        self.revision = 1
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
        while True:
            if self.waiting_ack:
                continue
            self.lock.acquire()
            operation = self.waiting.get()
            request = self.create_request(operation)
            self.sender.send(request.encode())
            self.waiting_ack = operation
            self.lock.release()

    def receive(self):
        while self.connected:
            try:
                sock, addr = self.receiver.accept()
                response = self.get_response(sock)
                if response['operation'] == 'ack':
                    self.lock.acquire()
                    self.waiting_ack = None
                    self.lock.release()
                else:
                    operation = response['operation']
                    self.apply_changes(operation)
            except socket.error:
                pass

    def apply_changes(self, operation):
        pass

    def create_request(self, operation):
        dict = {
            'server_id': self.file_id,
            'user_id': self.guid,
            'operation': operation.to_json,
            'revision': self.revision
        }
        return json.dumps(dict)

    def get_response(self, sock):
        data = []
        while True:
            r = sock.recv(1024)
            if not r:
                break
            data.append(r.decode())
        return json.loads(''.join(data))

    def connect_to_server(self):
        pass

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
                        sock.close()
                    break

        return Thread(target=create_server_function).start


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = Client()
    a = TextEditor(client)
    sys.exit(app.exec_())
