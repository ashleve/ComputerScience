import socket
import time


class Client:

    def __init__(self):
        self._socket = None

    def initialize_socket(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    def set_broadcast(self):
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def set_multicast(self):
        self._socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        self._socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

    def send_broadcast(self, message, port):
        self._socket.sendto(message.encode(), ("<broadcast>", port))
        print("Broadcast message sent:", message)

    def send_multicast(self, message, ip, port):
        self._socket.sendto(message.encode(), (ip, port))
        print("Multicast message sent:", message)

    def close_all(self):
        if self._socket is not None:
            self._socket.close()


def main():
    client = Client()
    try:
        client.initialize_socket()
    except socket.error:
        print("Initializing socket failed.")
        return

    choice = input("What do you want to do? (1 - send broadcast, 2 - send multicast): ")
    if choice == "1":
        client.set_broadcast()
        while True:
            try:
                client.send_broadcast("This is broadcast message.", port=7)
            except socket.error:
                print("Sending data failed.")
                break
            time.sleep(1)
    elif choice == "2":
        client.set_multicast()
        while True:
            ip = input("Type IP of multicast group: ")
            port = int(input("Type port number: "))
            try:
                client.send_multicast("This is broadcast message.", ip=ip, port=port)
            except socket.error:
                print("Sending data failed.")
                break

    client.close_all()


if __name__ == "__main__":
    main()
