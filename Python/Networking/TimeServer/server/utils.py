from datetime import datetime, timedelta
import threading
import struct
import socket


def get_addresses_of_all_interfaces():
    """
        This just lists the addresses of the interfaces that are attached to the outside world, not all interfaces.
    """
    ipv6_addresses = [addr[4][0] for addr in socket.getaddrinfo(socket.gethostname(), None, family=socket.AF_INET6)]
    ipv4_addresses = [addr[4][0] for addr in socket.getaddrinfo(socket.gethostname(), None, family=socket.AF_INET)]
    return ipv6_addresses, ipv4_addresses


def set_tcp_sockets(ip_addresses):
    sockets = []
    for addr in ip_addresses:
        sock = socket.socket(
            socket.AF_INET,  # IPv4
            socket.SOCK_STREAM  # TCP
        )
        sock.bind((addr, 0))  # bind to random port
        sockets.append(sock)
    return sockets


def listen_continuously(sock):
    sock.listen()
    while True:
        conn, addr = sock.accept()
        print("Connected to client socket:", addr)
        thread = threading.Thread(target=client_thread, args=(conn,), daemon=True)
        thread.start()


def client_thread(conn):
    try:
        while True:
            message = conn.recv(1024)
            if message == b"TIME REQUEST":
                current_time = datetime.now()
                # current_time += timedelta(seconds=3)  # add 3 seconds for testing
                message = str(current_time)
                conn.send(message.encode())

                message = conn.recv(1024)

            if message == b"STOP":
                break
    except socket.error:
        pass

    print("Client disconnected")
    conn.close()


def multicast_response_loop(multicast_sock, sockets):
    while True:
        message, (host, port) = multicast_sock.recvfrom(1024)
        if message == b"DISCOVERY":
            for s in sockets:
                answer = "OFFER ADDRESS PORT " + str(s.getsockname())
                multicast_sock.sendto(answer.encode(), (host, port))


def init_multicast_socket():
    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 7

    sock = socket.socket(
        socket.AF_INET,  # IPv4
        socket.SOCK_DGRAM,  # UDP
        socket.IPPROTO_UDP
    )

    # allow reuse of socket (to allow another instance of python running this script binding to the same ip/port)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # on this port, receives ALL multicast groups
    sock.bind(('', MCAST_PORT))

    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    return sock
