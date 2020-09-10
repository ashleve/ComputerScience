from utils import init_multicast_socket, multicast_response_loop, get_addresses_of_all_interfaces, set_tcp_sockets, \
    listen_continuously
import threading


def main():
    ipv6_addresses, ipv4_addresses = get_addresses_of_all_interfaces()
    sockets = set_tcp_sockets(ipv4_addresses)

    print("Server is listening on the following addresses:")
    for sock in sockets:
        thread = threading.Thread(target=listen_continuously, args=(sock,), daemon=True)
        thread.start()
        print(sock.getsockname())

    multicast_sock = init_multicast_socket()
    multicast_thread = threading.Thread(target=multicast_response_loop, args=(multicast_sock, sockets), daemon=True)
    multicast_thread.start()

    multicast_thread.join()

    multicast_sock.close()
    for sock in sockets:
        sock.close()


if __name__ == "__main__":
    main()
