import socket

# read the file
filename = 'file.txt'
with open(filename, 'r') as f:
    file_data = f.read()
    print("file is open")

# set up TCP connection
server_IP_address = 'localhost'
server_port = 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("socket created")
try:
    s.connect((server_IP_address, server_port))
    print("connection established")
except socket.error as err:
    print("Connection failed with error %s" % err)
    s.close()
    exit()

data_size = len(file_data)
half_size = data_size // 2

# send first half of the file
first_half = file_data[:half_size]
sent_size = 0
while sent_size < half_size:
    data_to_send = first_half[sent_size:sent_size + 1024]
    s.sendall(data_to_send.encode())
    sent_size += len(data_to_send)
print("### Sent the 1st data ###")

# wait for authentication from receiver
print("wait for authentication ")
auth = s.recv(1024)
print("auth: ", auth.decode())
xor_ans = 1101011111001001  # 9150 ^ 4699 = 10001110111110 ^ 1001001011011 = 1101011111001001
if auth != b'xor_ans':
    print('Authentication failed')
    s.close()
else:
    print('Authentication successful')

# switch to cubic congestion control algorithm
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, 'cubic'.encode())
print("*** change Algo: CUBIC ***")

# send second half of the file
second_half = file_data[half_size:]
sent_size = 0
while sent_size < len(second_half):
    data_to_send = second_half[sent_size:sent_size+1024]
    s.sendall(data_to_send.encode())
    sent_size += len(data_to_send)
print("### Sent the 2nd data ###")

# ask user if they want to send the file again
send_again = input('Send the file again? (y/n): ')
while send_again.lower() == 'y':
    # notify receiver
    s.sendall(b'Send again')

    # switch back to reno congestion control algorithm
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, 'reno'.encode())
    print("*** change Algo: RENO ***")

    # send first half of the file again
    sent_size = 0
    while sent_size < half_size:
        data_to_send = first_half[sent_size:sent_size + 1024]
        s.sendall(data_to_send.encode())
        sent_size += len(data_to_send)
    print("### Sent the 1st data ###")

    # wait for authentication from receiver
    auth = s.recv(1024)
    print("auth: ", auth.decode())
    xor_ans = 1101011111001001  # 9150 ^ 4699 = 10001110111110 ^ 1001001011011 = 1101011111001001
    if auth != b'xor_ans':
        print('Authentication failed')
        s.close()
    else:
        print('Authentication successful')

    # switch to cubic congestion control algorithm
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, 'cubic'.encode())
    print("*** change Algo: CUBIC ***")

    # send second half of the file again
    sent_size = 0
    while sent_size < len(second_half):
        data_to_send = second_half[sent_size:sent_size + 1024]
        s.sendall(data_to_send.encode())
        sent_size += len(data_to_send)
    print("### Sent the 2nd data ###")

    # ask user if they want to send the file again
    send_again = input('Send the file again? (y/n): ')

# send exit message
print("GoodBy!!! :)")
# close the connection
s.close()
