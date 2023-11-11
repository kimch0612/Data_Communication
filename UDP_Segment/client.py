import socket
import os

client_address = ('192.168.50.60', 5555)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
file_path = 'test.png'
file_name = os.path.basename(file_path)
client_socket.sendto(file_name.encode('utf-8'), client_address)
file_size = os.path.getsize(file_path)
client_socket.sendto(str(file_size).encode('utf-8'), client_address)

with open(file_path, 'rb') as file:
    data = file.read(13738)
    while data:
        client_socket.sendto(data, client_address)
        data = file.read(13738)

print("Done.")