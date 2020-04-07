import socket


class Server:

    DEFAULT_HOST = '127.0.0.1'              # The server's hostname or IP address
    DEFAULT_PORT = 7                        # The port used by the server

    def __init__(self):
        self._socket = None

    def initialize_socket(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self._socket.bind((host, port))
        self._socket.listen()
        conn, addr = self._socket.accept()
        return conn, addr

    @staticmethod
    def echo_service(conn, addr):
        while True:

            try:
                data = conn.recv(1024).decode()
            except socket.error:
                print("Receiving data failed.")
                return False

            if not data:
                print("Client disconnected.")
                return True

            print("Received data from address:", addr, "data:", data, "size of data:", data.__sizeof__())

            try:
                conn.send(data.encode())
            except socket.error:
                print("Sending data failed.")
                return False

            print("Data sent back.", end="\n\n")

    def close_all(self):
        if self._socket is not None:
            self._socket.close()
