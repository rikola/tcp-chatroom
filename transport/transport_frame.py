import struct


# Format chars are defined here https://docs.python.org/3.9/library/struct.html#format-characters
TRANSPORT_FRAME_FORMAT: str = '!Ip'
'''Format string for marshalling a `TCPFrame` instance to binary'''

TRANSPORT_FRAME_SIZE = struct.calcsize(TRANSPORT_FRAME_FORMAT)
'''Total size in bytes of the marshalled `TCPFrame`'''


class TransportFrame:
    '''Represents a message being transmitted over a TCP socket connection'''
    message: str

    def __init__(self, message: str):
        self.message = message

    def __eq__(self, other):
        return self.message == other.message

    def build(self) -> bytes:
        packet = struct.pack(
            TRANSPORT_FRAME_FORMAT,
            TRANSPORT_FRAME_SIZE,
            self.message.encode()
        )
        return packet


def unmarshall(data: bytes) -> TransportFrame:
    if len(data) != TRANSPORT_FRAME_SIZE:
        raise ValueError("Malformed message data. Wrong size.")
    size, msg_bytes = struct.unpack(TRANSPORT_FRAME_FORMAT, data)
    message: str = msg_bytes.decode()
    return TransportFrame(message)
