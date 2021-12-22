import asyncio
from queue import Queue
import json
import uuid

from common.operations_converter import convert_operation
'''
    insert pos text
'''


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.revision_log = {}
        self.pending_processing = Queue()
        self.doc_state = {}
        self.connected_users = {}

    async def handle_client(self, reader, writer):
        while True:
            request = []
            while True:
                data = (await reader.read(1024)).decode('utf8')
                if not data:
                    break
                request.append(data)
            request = json.loads("".join(request))
            # if operation == "close":
            #     pass
            self.pending_processing.put((writer, request))

    def process_requests(self):
        writer, request = self.pending_processing.get()
        server_id, user, operation, request_revision = \
            request["server_id"], request["user"], request["operation"], \
            request["revision"]
        previous_operation = self.revision_log[server_id][-1]
        applied_operation = self.apply_operation(operation,
                                                 previous_operation,
                                                 self.doc_state[server_id])
        revision = request_revision + 1
        self.send_to_users(writer, applied_operation, revision, server_id)

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

    def apply_operation(self, previous_operation, operation, text):
        operation_to_perform = convert_operation(operation,
                                                  previous_operation)
        if operation_to_perform is InsertOperation:
            self.insert(operation, text)
        else:
            self.delete(operation, text)
        return operation_to_perform

    def insert(self, operation: InsertOperation, text: str) -> str:
        return f"{text[:operation.index]}{operation.symbol}" \
               f"{text[operation.index:]}"

    def delete(self, operation: DeleteOperation, text: str) -> str:
        return f"{text[:operation.index]}{text[operation.index + 1:]}"

    def connect(self, operation):
        pass

    def create_server(self, operation):
        id = uuid.uuid1()
        self.revision_log[id] = []
        # self.pending_processing[id] = Queue()
        self.doc_state[id] = operation["data"]
        self.connected_users[id] = [operation["user"]]
        return None


async def start_server():
    server = Server('localhost', 5000)
    async with await asyncio.start_server(server.handle_client, server.ip, server.port) as s:
        await s.serve_forever()

asyncio.run(start_server())

