import socket

HOST = 'localhost'
PORT = 8080
# read the file
filename = 'file.txt'
with open(filename, 'r') as f:
    file_data = f.read()
    print("file is open")

data_size = len(file_data)
half_size = data_size // 2
first_half = file_data[:half_size]
second_half = file_data[half_size:]

# set up TCP connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("socket created")
sock.connect((HOST, PORT))
print("connection established")

# sets the size of the buffer that the socket will use to send data
sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 32768)
# set the TCP_NODELAY option to 1 to disables the Nagle algorithm for this socket
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

while True:
    # Change the CC Algorithm back to reno
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, 'reno'.encode())
    print("*** change Algo: RENO ***")

    # send first half of the fileS
    sock.sendall(first_half.encode())
    # sent = 0
    # while sent < len(first_half):
    #     sent += sock.send(first_half.encode())
    print("### Sent the 1st data ###")

    # wait for authentication from receiver
    print("wait for authentication ")
    auth = sock.recv(1024)
    xor_ans = 9150 ^ 4699  # 9150 ^ 4699 = 10001110111110 ^ 1001001011011 = 1101011111001001
    print("auth: ", auth.decode())
    print("xor_ans: ", xor_ans)
    if auth != b'xor_ans':
        print('Authentication failed')
        sock.close()
        print("socket closes")
        break
    else:
        print('Authentication successful')

        # switch to cubic congestion control algorithm
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, 'cubic'.encode())
        print("*** change Algo: CUBIC ***")

        # send second half of the file
        sock.sendall(second_half.encode())
        # sent = 0
        # while sent < len(second_half):
        #     sent += sock.send(second_half.encode())
        print("### Sent the 2nd data ###")
        print("")

    # ask user if they want to send the file again
    send_again = input('Send the file again? (y/n): ')
    if send_again.lower() != 'y':
        # send exit message
        sock.sendall("Stop sending".encode())
        print("GoodBye!!!")
        # close the connection
        print("socket closes")
        sock.close()
        break

    else:
        sock.sendall("keep Sending".encode())
        print("Keep sending")
