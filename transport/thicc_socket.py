import socket

MSG_LEN = 2048


class ThiccSocket:
    """Keeps alive an individual socket connection.
    For transfers that may overflow a single TCP size limit."""

    def __init__(self, sock: socket.socket = None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg):
        totalsent = 0
        while totalsent < MSG_LEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent += sent

    def receive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSG_LEN:
            chunk = self.sock.recv(min(MSG_LEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd += len(chunk)
        return b''.join(chunks)
