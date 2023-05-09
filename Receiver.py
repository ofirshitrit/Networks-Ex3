import socket
import time

# Define the IP address and port number for the receiver
HOST = 'localhost'
PORT = 8080
HALF_SIZE = 1310720

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Create a socket succeed")

# Bind the socket to a specific address and port number
sock.bind((HOST, PORT))
print("Bind succeed")

# Listen for incoming connections
sock.listen()
print("ready to receive files")

# Wait for a connection
conn, addr = sock.accept()
print(f'Connected by {addr}')

# Change the CC Algorithm back to reno
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, 'reno'.encode())
print("*** change Algo: RENO ***")

# Receive the first part of the file
start_time = time.time()  # start measuring time
received_data = b''
_sum = 0
while True:
    data = conn.recv(1024)
    _sum += len(data)
    if _sum == HALF_SIZE:
        break
    received_data += data
print("### Receive the 1st data  ### ")
part1_time = time.time() - start_time

# Send back an authentication message
xor_ans = 1101011111001001  # 9150 ^ 4699 = 10001110111110 ^ 1001001011011 = 1101011111001001
conn.sendall(b'xor_ans')
print("Authentication successful")

# Change the CC Algorithm to cubic
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, 'cubic'.encode())
print("*** Algo: CUBIC ***")

# Receive the second part of the file
start_time = time.time()  # start measuring time
received_data = b''
_sum = 0
while True:
    data = conn.recv(1024)
    _sum += len(data)
    if _sum == HALF_SIZE:
        break
    received_data += data
part2_time = time.time() - start_time
print("### Receive the 2nd data  ### ")

# Check if the sender wants to send the file again
while True:
    # Ask the user if they want to send the file again
    user_input = input('Do you want to receive the file again? (y/n): ')

    if user_input.lower() == 'y':
        # Send a notification to the sender that the receiver is ready for another transfer
        xor_ans = 1101011111001001  # 9150 ^ 4699 = 10001110111110 ^ 1001001011011 = 1101011111001001
        conn.sendall(b'xor_ans')

        # Change the CC Algorithm back to reno
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, 'reno'.encode())
        print("*** change Algo: RENO ***")

        # Receive the first part of the file
        start_time = time.time()  # start measuring time
        received_data = b''
        _sum = 0
        while True:
            data = conn.recv(1024)
            _sum += len(data)
            if _sum == HALF_SIZE:
                break
            received_data += data
        print("### Receive the 1st data  ### ")
        part1_time += time.time() - start_time

        # Change the CC Algorithm to cubic
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, 'cubic'.encode())
        print("*** Algo: CUBIC ***")

        # Receive the second part of the file
        start_time = time.time()  # start measuring time
        received_data = b''
        _sum = 0
        while True:
            data = conn.recv(1024)
            _sum += len(data)
            if _sum == HALF_SIZE:
                break
            received_data += data
        print("### Receive the 2st data  ### ")
        part2_time += time.time() - start_time

    elif user_input.lower() == 'n':
        # Print out the times for each part of the file
        print('Time to receive first part with RENO:', part1_time)
        print('Time to receive second part with CUBIC:', part2_time)

        # Calculate the average time for each part of the file
        avg_part1_time = part1_time / 5
        avg_part2_time = part2_time / 5

        # Print the average time
        print('Average time to receive first part:', avg_part1_time)
        print('Average time to receive second part:', avg_part2_time)

        # Close the connection
        conn.close()
        break

    else:
        print('Invalid input. Please enter y or n.')