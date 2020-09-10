from ast import literal_eval as make_tuple
from datetime import datetime
import socket
import time


def load_last_server_info():
    with open("last_server.txt", "r") as file:
        text = file.readline()
    try:
        last_server = make_tuple(text)
    except Exception:
        last_server = None

    return last_server


def get_default_server(host_list, last_server):
    default_choice = 0
    for i, host in enumerate(host_list):
        if last_server is not None and last_server == host:
            default_choice = i

    return default_choice


def print_all_servers(host_list, default_choice):
    for i, host in enumerate(host_list):
        if i == default_choice:
            print(f"{i} - {host} [DEFAULT]")
        else:
            print(f"{i} - {host}")


def init_multicast_socket():
    # regarding socket.IP_MULTICAST_TTL
    # ---------------------------------
    # for all packets sent, after two hops on the network the packet will not
    # be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
    MULTICAST_TTL = 2

    sock = socket.socket(
        socket.AF_INET,  # IPv4
        socket.SOCK_DGRAM,  # UDP
        socket.IPPROTO_UDP
    )
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

    return sock


def send_discovery(sock):
    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 7
    sock.sendto(b"DISCOVERY", (MCAST_GRP, MCAST_PORT))


def get_host_list(multicast_sock):
    multicast_sock.settimeout(1)
    waiting_time = 3

    host_list = []
    start = time.time()
    while time.time() - start < waiting_time:
        try:
            message, (host, port) = multicast_sock.recvfrom(1024)
            if "OFFER ADDRESS PORT" in message.decode():
                address = make_tuple(message.decode().replace("OFFER ADDRESS PORT ", ""))  # parse address
                host_list.append(address)
        except socket.timeout:
            pass

    return host_list


def connect_to_server(host, port):
    sock = socket.socket(
        socket.AF_INET,  # IPv4
        socket.SOCK_STREAM  # TCP
    )
    sock.connect((host, port))
    print("Connected on client socket:", sock.getsockname(), "to server socket:", str((host, port)))

    return sock


def download_time(sock):
    t1 = datetime.now()

    message = b"TIME REQUEST"
    sock.send(message)

    server_time = datetime.strptime(sock.recv(1024).decode(), '%Y-%m-%d %H:%M:%S.%f')
    client_time = t2 = datetime.now()

    delta = server_time + (t2 - t1)/2 - client_time
    real_server_time = server_time + delta

    delta_milliseconds = delta.total_seconds() * 10**3

    return real_server_time, delta_milliseconds

