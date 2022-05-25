import socket

class MyDevice(object):

    def __init__(self, ip, port=4011):
        self.ip = ip
        self.port = port
        self.socket = None
        self.sent = 0

    def connect(self, timeout=1.0):
        """ Connects to device, throws exception if can't connect """
        if self.socket:
            self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(timeout)
        self.socket.connect((self.ip, self.port))

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    def send(self, msg):
        if not self.socket:
            raise RuntimeError("not connected")

        # TODO: send() doesn't guarantee sending entire message
        sent = self.socket.send(msg)
        if sent == 0:
            self.disconnect()
            raise RuntimeError("socket connection broken")

        self.sent += sent