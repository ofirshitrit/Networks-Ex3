import socket

HOST = 'localhost'
PORT = 9999
# read the file
filename = 'file.txt'
with open(filename, 'r') as f:
    file_data = f.read()
    print("file is open")

data_size = len(file_data)
half_size = data_size // 2
first_half = file_data[:half_size]
second_half = file_data[half_size:]


def create_connection() -> socket:
    # set up TCP connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("socket created")
    sock.connect((HOST, PORT))
    print("connection established")
    return sock


def send_file():
    sent_size = 0
    while sent_size < half_size:
        data_to_send = first_half[sent_size:sent_size + 1024]
        sock.sendall(data_to_send.encode())
        sent_size += len(data_to_send)


while True:
    # set up TCP connection
    sock = create_connection()

    # Change the CC Algorithm back to reno
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, 'reno'.encode())
    print("*** change Algo: RENO ***")

    # send first half of the file
    send_file()
    print("### Sent the 1st data ###")
    sock.close()
    print("socket closes")

    # set up TCP connection
    sock = create_connection()

    # wait for authentication from receiver
    print("wait for authentication ")
    auth = sock.recv(10)
    xor_ans = 9150 ^ 4669  # 9150 ^ 4699 = 10001110111110 ^ 1001001011011 = 1101011111001001
    print("auth: ", auth.decode())
    print("ans_xor: ", xor_ans)
    if auth != b'xor_ans':
        print('Authentication failed')
        sock.close()
        print("socket closes")
        break
    else:
        print('Authentication successful')

        # set up TCP connection
        sock = create_connection()

        # switch to cubic congestion control algorithm
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, 'cubic'.encode())
        print("*** change Algo: CUBIC ***")

        # send second half of the file
        send_file()
        print("### Sent the 2nd data ###")
        sock.close()
        print("socket closes")

    # ask user if they want to send the file again
    send_again = input('Send the file again? (y/n): ')
    if send_again.lower() != 'y':
        # set up TCP connection
        sock = create_connection()

        # send exit message
        sock.sendall("Stop sending".encode())
        print("GoodBye!!! :)")

        # close the connection
        print("socket closes")
        sock.close()
        break

    else:
        # set up TCP connection
        sock = create_connection()

        sock.sendall("keep Send".encode())
        sock.close()
        print("socket closes")
