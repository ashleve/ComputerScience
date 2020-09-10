from utils import send_discovery, get_host_list, init_multicast_socket, connect_to_server, download_time, \
    load_last_server_info, get_default_server, print_all_servers
import socket
import time


def main():
    multicast_sock = init_multicast_socket()

    last_server = load_last_server_info()

    while True:

        print("Gathering server responses...")
        send_discovery(multicast_sock)
        host_list = get_host_list(multicast_sock)
        print(f"Number of available servers: {len(host_list)}")

        if len(host_list) == 0:
            continue

        default_choice = get_default_server(host_list, last_server)

        print("Choose server:")
        print_all_servers(host_list, default_choice)
        choice = input()
        choice = default_choice if choice == "" else choice
        try:
            choice = int(choice)
        except ValueError:
            print("Incorrect choice.")
            continue
        if not 0 <= choice < len(host_list):
            print("Incorrect choice.")
            continue

        print("Enter time request interval (10-1000)[ms]:")
        try:
            repeat_time_interval = int(input())
        except ValueError:
            print("Incorrect request time interval.")
            continue
        if not 10 <= repeat_time_interval <= 1000:
            print("Incorrect request time interval.")
            continue

        try:
            sock = connect_to_server(host=host_list[choice][0], port=host_list[choice][1])
        except ConnectionRefusedError:
            print("Error: Connection refused.")
            continue

        break

    multicast_sock.close()

    with open("last_server.txt", "w") as file:
        file.write(str(host_list[choice]))

    try:
        repeat = True
        while True:
            server_time, delta = download_time(sock)
            print(f"Server time: {server_time}")
            print(f"Client/Server time difference [ms]: {delta}")

            if not repeat:
                sock.send(b"STOP")
                break

            time.sleep(repeat_time_interval / 1000)
            sock.send(b"REPEAT")

    except socket.error:
        print("Communication with server failed.")

    sock.close()


if __name__ == "__main__":
    main()
