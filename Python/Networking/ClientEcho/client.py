import socket


class Client:

    DEFAULT_HOST = '127.0.0.1'              # The server's hostname or IP address
    DEFAULT_PORT = 7                        # The port used by the server

    def __init__(self):
        self._socket = None

    def initialize_socket(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self._socket.connect((host, port))

    def echo_service(self):
        while True:
            print("Type your message (type 'stop' to quit): ", end="")
            data_out = ""
            while data_out == "":   # prevent sending empty message
                data_out = input()
            data_out = data_out.encode()

            try:
                self._socket.sendall(data_out)
            except socket.error:
                print("Sending data failed.")
                return

            print("Number of bytes send:", data_out.__sizeof__())

            try:
                data_in = self._socket.recv(2024)
            except socket.error:
                print("Receiving data failed.")
                return

            data_in_decoded = data_in.decode()
            print("Message received:", data_in_decoded)
            print("Number of bytes received:", data_in.__sizeof__(), end="\n\n")

            if data_in_decoded == "STOP" or data_in_decoded == "stop":
                return

    def close_all(self):
        if self._socket is not None:
            self._socket.close()
