import socket
import threading


class ClientHandle:

    def __init__(self, conn, addr, server):
        self._stop_event = threading.Event()        # thread termination condition
        self.conn = conn
        self.addr = addr
        self.server = server

    def stop(self):
        self._stop_event.set()

    def echo_service(self):
        """
            This is run as thread. It checks termination condition after every second.
        """
        self.conn.settimeout(1.0)
        while not self._stop_event.is_set():        # exit on signal from caller
            success = self.handle_data()            # handle any data; continue loop after 1 second
            if not success:
                self.conn.close()
                self.server.clients.remove(self)
                break

    def handle_data(self):
        try:
            data = self.conn.recv(1024)
            if not data:
                print("Client disconnected.")
                return False

            print(
                "Received data from address:", self.addr,
                "\ndata:", data.decode(),
                "\nsize of data:", data.__sizeof__()
            )

            self.conn.send(data)

        except socket.timeout:
            return True
        except socket.error:
            return False

        print("Data sent back.", end="\n\n")
        return True


class Server:

    DEFAULT_HOST = '127.0.0.1'              # The server's hostname or IP address
    DEFAULT_PORT = 7                        # The port used by the server
    MAX_NUM_OF_CLIENTS = 1

    def __init__(self):
        self._socket = None
        self.clients = []                   # List of all client threads currently running

    def initialize_server(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((host, port))
        self._socket.listen(Server.MAX_NUM_OF_CLIENTS)

    def accept(self):
        conn, addr = self._socket.accept()
        return conn, addr

    def create_client_thread(self, conn, addr):
        if len(self.clients) >= Server.MAX_NUM_OF_CLIENTS:
            try:
                conn.recv(1024)
                message = "Server is busy, too many clients."
                conn.send(message.encode())
                conn.close()
                return
            except socket.error:
                return

        client = ClientHandle(conn, addr, self)
        threading.Thread(target=client.echo_service, args=()).start()
        self.clients.append(client)
        return client

    def remove_disconnected_clients_from_list(self):
        for client in self.clients:
            if client.disconnected:
                self.clients.remove(client)

    def close_all(self):
        for client in self.clients:
            client.stop()
            client.conn.close()

        if self._socket is not None:
            self._socket.close()
