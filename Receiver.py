import socket
import time

# Define the IP address and port number for the receiver
HOST = 'localhost'
PORT = 9999
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

# Create list to save the times
reno_time = []
cubic_time = []
number_of_sends = 0

# Change the CC Algorithm back to reno
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, 'reno'.encode())
print("*** change Algo: RENO ***")

# Receive the first part of the file
start_time = time.time()  # start measuring time
received_data = b''
_sum = 0
while True:
    data = conn.recv(2048)
    _sum += len(data)
    if _sum == HALF_SIZE:
        break
    received_data += data
print("### Receive the 1st data  ### ")
part1_time = time.time() - start_time
reno_time.append(part1_time)
# number_of_sends += 1

# Send back an authentication message
xor_ans = 1101011111001001  # 9150 ^ 4699 = 10001110111110 ^ 1001001011011 = 1101011111001001
conn.sendall(b'xor_ans')
print("Authentication successful")

# Change the CC Algorithm to cubic
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, 'cubic'.encode())
print("*** change Algo: CUBIC ***")

# Receive the second part of the file
start_time = time.time()  # start measuring time
received_data = b''
_sum = 0
while True:
    data = conn.recv(2048)
    _sum += len(data)
    if _sum == HALF_SIZE:
        break
    received_data += data
part2_time = time.time() - start_time
print("### Receive the 2nd data  ### ")
cubic_time.append(part2_time)
number_of_sends += 1

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
            data = conn.recv(2048)
            _sum += len(data)
            if _sum == HALF_SIZE:
                break
            received_data += data
        print("### Receive the 1st data  ### ")
        part1_time += time.time() - start_time
        reno_time.append(part1_time)
        # number_of_sends += 1

        # Change the CC Algorithm to cubic
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, 'cubic'.encode())
        print("*** change Algo: CUBIC ***")

        # Receive the second part of the file
        start_time = time.time()  # start measuring time
        received_data = b''
        _sum = 0
        while True:
            data = conn.recv(2048)
            _sum += len(data)
            if _sum == HALF_SIZE:
                break
            received_data += data
        print("### Receive the 2st data  ### ")
        part2_time += time.time() - start_time
        cubic_time.append(part2_time)
        number_of_sends += 1

    elif user_input.lower() == 'n':
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

        # Close the connection
        conn.close()
        break

    else:
        print('Invalid input. Please enter y or n.')