import asyncio
from queue import Queue


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.revision_log = []
        self.pending_processing = Queue()

    def handle_client(self, reader, writer):
        request = (await reader.read(255)).decode('utf8')
        print('request, ', request)
        response = 'Hi!!\n'.encode()
        writer.write(response)
        await writer.drain()
        writer.close()


class Operation:
    def __init__(self, type, value, index):
        self.type = type
        self.value = value
        self.index = index


class InsertOperation(Operation):
    pass

class RemoveOperation(Operation):
    pass


if __name__ == '__main__':
    server = Server('localhost', 5000)
    async with await asyncio.start_server(server.handle_client, server.ip, server.port) as s:
        s.serve_forever()
