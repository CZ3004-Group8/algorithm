import pickle
import socket
import sys

from algorithm import settings


class RPiConnection:
    HOST = settings.HOST
    PORT = settings.PORT

    def __init__(self):
        self.socket = socket.socket()
        self.socket.settimeout(5)

    def connect(self):
        try:
            print("Attempting to connect to RPi...")
            self.socket.connect((self.HOST, self.PORT))
            print(f"Connected to RPi at (host={self.HOST}, port={self.PORT})")
        except OSError as e:
            print(f"Unable to connect: {e}")
            sys.exit(1)

    def send_message(self, obj):
        # This may allow arbitrary code execution. Only connect to trusted connections!!!
        self.socket.sendall(pickle.dumps(obj))
