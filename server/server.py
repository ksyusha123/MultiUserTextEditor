import asyncio
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
            previous_operation = self.revision_log[1][-1] if len(self.revision_log) != 0 else None
            applied_operation = self.apply_operation(operation)
            revision = None  # request_revision + 1
            self.send_to_users(writer, applied_operation, revision, 1)

    def send_to_users(self, writer, applied_operation, revision, server_id):
        ack = {"operation": "ack",
               "revision": revision}
        to_send = {"operation": applied_operation.to_dict(),
                   "revision": revision}
        sin = json.dumps(to_send)
        for user in self.connected_users[server_id]:
            if user == writer:
                writer.write(json.dumps(ack))
            user.write(sin)

    def apply_operation(self, request, previous_operation=None, text=None):
        operation = request['operation']
        if type(operation) is CreateServerOperation:
            id = self.create_server(operation)
            self.lock.acquire()
            self.doc_state[id] = operation.file
            self.connected_users[id] = [request['user_id']]
            self.lock.release()
            return operation

        operation_to_perform = convert_operation(operation,
                                                 previous_operation)
        if type(operation_to_perform) is InsertOperation:
            self.insert(operation, text)
        else:
            self.delete(operation, text)
        return operation_to_perform

    def insert(self, operation: InsertOperation, text: str) -> str:
        return f"{text[:operation.index]}{operation.text}" \
               f"{text[operation.index:]}"

    def delete(self, operation: DeleteOperation, text: str) -> str:
        return f"{text[:operation.index]}{text[operation.index + 1:]}"

    def create_server(self, operation):
        id = uuid.uuid1()
        self.revision_log[id] = []
        self.pending_processing = Queue()
        self.doc_state[id] = operation.file
        return id


async def start_server():
    server = Server('localhost', 5000)
    async with await asyncio.start_server(server.handle_client, server.ip, server.port) as s:
        await s.serve_forever()


asyncio.run(start_server())
