import socket
import time

HOST = 'localhost'
PORT = 9999
HALF_SIZE = 1310720
reno_time = []
cubic_time = []
number_of_sends = 0


def print_times():
    print("Times: ")
    # Print out the times for each part of the file
    for i in range(number_of_sends):
        print('Time to receive first part with RENO:', reno_time[i])
        print('Time to receive second part with CUBIC:', cubic_time[i])

    print("Average: ")
    # Calculate the average time for each part of the file
    avg_part1_time = part1_time / 5
    avg_part2_time = part2_time / 5
    print('Average time to receive first part with RENO:', avg_part1_time)
    print('Average time to receive second part with CUBIC:', avg_part2_time)


def create_socket() -> socket:
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Create a socket succeed")

    # Bind the socket to a specific address and port number
    sock.bind((HOST, PORT))
    print("Bind succeed")

    # Listen for incoming connections
    sock.listen()
    print("ready to receive files")
    return sock


def receive_file():
    while True:
        data = conn.recv(2048)
        if len(data) <= 0:
            break


sock = create_socket()

while True:
    # Wait for a connection
    conn, addr = sock.accept()
    print(f'Connected by {addr}')

    # Change the CC Algorithm back to reno
    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, 'reno'.encode())
    print("*** change Algo: RENO ***")

    # Receive the first part of the file
    start_time = time.time()  # start measuring time
    receive_file()
    print("### Receive the 1st data  ### ")
    part1_time = time.time() - start_time
    reno_time.append(part1_time)

    # Wait for a connection
    conn, addr = sock.accept()
    print(f'Connected by {addr}')

    # Send back an authentication message
    xor_ans = 9150 ^ 4699  # 9150 ^ 4699 = 10001110111110 ^ 1001001011011 = 1101011111001001
    conn.sendall(b'xor_ans')
    print("Authentication sent")
    conn.close()
    print("connection close")

    conn, addr = sock.accept()
    print(f'Connected by {addr}')

    # Change the CC Algorithm to cubic
    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, 'cubic'.encode())
    print("*** change Algo: CUBIC ***")

    # Receive the second part of the file
    start_time = time.time()  # start measuring time
    receive_file()
    part2_time = time.time() - start_time
    print("### Receive the 2nd data  ### ")
    cubic_time.append(part2_time)
    number_of_sends += 1
    conn.close()
    print("connection close")

    conn, addr = sock.accept()
    print(f'Connected by {addr}')

    finish_sending = conn.recv(10).decode()
    if finish_sending != "keep Send":
        print_times()
        break
    else:
        conn.close()
        print("connection close")
