import asyncio
from queue import Queue
import json
import uuid
'''
    insert pos text
'''


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.revision_log = {}
        self.pending_processing = {}
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
            operation = json.loads("".join(request))
            if operation["name"] == "close":
                pass
            ack = self.apply_operation(operation)
            writer.write(json.dumps(ack))
            operation["revision"] = ack["revision"]
            sin = json.dumps(operation)
            for user in self.connected_users:
                if user == writer:
                    continue
                user.write(sin)

    def apply_operation(self, operation):
        pass

    def insert(self, operation):
        pass

    def delete(self, operation):
        pass

    def connect(self, operation):
        pass

    def create_server(self, operation):
        id = uuid.uuid1()
        self.revision_log[id] = []
        self.pending_processing[id] = Queue()
        self.doc_state[id] = operation["data"]
        self.connected_users[id] = [operation["user"]]
        return None


async def start_server():
    server = Server('localhost', 5000)
    async with await asyncio.start_server(server.handle_client, server.ip, server.port) as s:
        await s.serve_forever()

asyncio.run(start_server())

