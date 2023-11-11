import socket
import os

server_address = ('192.168.50.60', 5555)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_address)

print(f"Server is now running on {server_address}..")

while True:
    filename, client_address = server_socket.recvfrom(13738)
    filename = filename.decode('utf-8')
    file_size, client_address = server_socket.recvfrom(13738)
    file_size = int(file_size.decode('utf-8'))

    print(f"File reception started. File name: {filename}, File size: {file_size} bytes")

    received_data_size = 0
    with open(filename, 'wb') as file:
        while received_data_size < file_size:
            data, client_address = server_socket.recvfrom(13738)
            file.write(data)
            received_data_size += len(data)

    print("Done.")