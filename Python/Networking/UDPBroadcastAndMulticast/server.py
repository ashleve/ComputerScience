import socket


class Server:
    """Server listens to broadcasts."""

    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5007

    def __init__(self):
        self._socket = None

    def initialize_socket(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def set_bind(self, port=MCAST_PORT):
        self._socket.bind(("", port))

    def set_multicast(self, multicast_group=MCAST_GRP):
        host = socket.gethostbyname(socket.gethostname())
        mreq = socket.inet_aton(multicast_group) + socket.inet_aton(host)
        self._socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def receive(self):
        data, addr = self._socket.recvfrom(1024)
        print(f"Received message: '{data.decode()}' from address: {addr}")

    def close_all(self):
        if self._socket is not None:
            self._socket.close()


def main():
    server = Server()
    try:
        server.initialize_socket()
    except socket.error:
        print("Initializing socket failed.")
        return

    choice = input("What do you want to do? (1 - listen for broadcasts, 2 - listen for multicasts): ")

    if choice == "1":
        server.set_bind(port=7)
    elif choice == "2":
        ip = input("Type multicast group: ")
        port = int(input("Type port number: "))
        try:
            server.set_bind(port=port)
            server.set_multicast(multicast_group=ip)
        except socket.error:
            print("Incorrect multicast group or port.")
            server.close_all()
            return
    else:
        server.close_all()
        return

    while True:
        try:
            server.receive()
        except socket.error:
            print("Receiving data failed.")
            break

    server.close_all()


if __name__ == "__main__":
    main()
