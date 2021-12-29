import asyncio
import socket
from queue import Queue
import json
import uuid
from threading import Thread, Lock

from common.operations_converter import convert_operation
from common.operations import *


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.revision_log = {}
        self.pending_processing = Queue()
        self.doc_state = {}
        self.connected_users = {}
        self.thread = Thread(target=self.process_requests).start()
        self.lock = Lock()
        self.previous_operation = None

    async def handle_client(self, reader, writer):
        while True:
            request = []
            while True:
                data = (await reader.read(1024)).decode('utf8')
                print(data)
                request.append(data)
                if len(data) < 1024:
                    break
            request = json.loads("".join(request))

            self.pending_processing.put((writer, request))

    def process_requests(self):
        while True:
            writer, request = self.pending_processing.get()
            # server_id, user, operation, request_revision = \
            #     request["server_id"], request["user"], request["operation"], \
            #     request["revision"]
            operation = request['operation']
            operation = operation_from_json(operation)
            request['operation'] = operation
            applied_operation = self.apply_operation(request, self.previous_operation)
            self.lock.acquire()
            self.previous_operation = operation
            self.lock.release()
            revision = None  # request_revision + 1
            self.send_to_users(request, applied_operation, revision, request['file_id'])

    def send_to_users(self, request, applied_operation, revision, file_id):
        ack = {"operation": "ack",
               "revision": revision,
               "file_id": file_id}
        to_send = {"operation": applied_operation.to_dict(),
                   "revision": revision}
        sin = json.dumps(to_send).encode()
        ack = json.dumps(ack).encode()
        for user in self.connected_users[file_id]:
            if request['user_id'] == user:
                self.connected_users[file_id][user].sendall(ack)
            else:
                self.connected_users[file_id][user].sendall(sin)

    def apply_operation(self, request, previous_operation, text=None):
        operation = request['operation']
        if type(operation) is CreateServerOperation:
            id = self.create_server(operation)
            self.lock.acquire()
            self.doc_state[id] = operation.file
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((request['addr'], 63201))
            self.connected_users[id] = {request['user_id']: sock}
            request['file_id'] = id
            self.lock.release()
            return operation

        operation_to_perform = convert_operation(operation,
                                                 previous_operation)
        if type(operation_to_perform) is InsertOperation:
            self.insert(operation, text)
        elif type(operation_to_perform) is DeleteOperation:
            self.delete(operation, text)
        return operation_to_perform

    def insert(self, operation: InsertOperation, text: str) -> str:
        return f"{text[:operation.index]}{operation.text}" \
               f"{text[operation.index:]}"

    def delete(self, operation: DeleteOperation, text: str) -> str:
        return f"{text[:operation.index]}{text[operation.index + 1:]}"

    def create_server(self, operation):
        id = str(uuid.uuid1())
        self.revision_log[id] = []
        self.pending_processing = Queue()
        self.doc_state[id] = operation.file
        return id



async def start_server():
    server = Server('localhost', 5000)
    async with await asyncio.start_server(server.handle_client, server.ip, server.port) as s:
        await s.serve_forever()


asyncio.run(start_server())
