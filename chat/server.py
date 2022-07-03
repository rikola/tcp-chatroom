import asyncio
import logging
from asyncio import StreamWriter, StreamReader

log = logging.getLogger(__name__)

clients = {}  # task -> (reader, writer)

writers: list[StreamWriter] = []


def forward(writer: StreamWriter, addr, message: str):
    for w in writers:
        if w != writer:
            w.write(f"{addr!r}: {message!r}\n".encode())


async def handle(reader: StreamReader, writer: StreamWriter):
    writers.append(writer)
    addr = writer.get_extra_info('peername')
    message = f"{addr!r} is now online!"
    print(message)
    forward(writer, addr, message)
    while True:
        data = await reader.readline()
        message = data.decode().strip()
        forward(writer, addr, message)
        await writer.drain()
        if message == "exit":
            message = f"{addr!r} is signing off..."
            print(message)
            forward(writer, "Server", message)
            break
    writers.remove(writer)
    writer.close()


async def main():
    server = await asyncio.start_server(handle, '127.0.0.1', 8888)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
