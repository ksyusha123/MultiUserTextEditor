import asyncio

ip = 'localhost'
port = 5000


def handle_client(reader, writer):
    request = (await reader.read(255)).decode('utf8')
    print('request, ', request)
    responce = 'Hi!!\n'.encode()
    writer.write(responce)
    await writer.drain()
    writer.close()


if __name__ == '__main__':
    server = await asyncio.start_server(handle_client, ip, port)
    async with server:
        server.serve_forever()
