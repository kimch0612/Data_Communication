import socket
import os

server_address = ('192.168.50.60', 5555)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
file_path = 'btn_logo_header.png'
file_name = os.path.basename(file_path)
client_socket.sendto(file_name.encode('utf-8'), server_address)

file_size = os.path.getsize(file_path)
client_socket.sendto(str(file_size).encode('utf-8'), server_address)

with open(file_path, 'rb') as file:
    data = file.read(1024)
    while data:
        client_socket.sendto(data, server_address)
        data = file.read(1024)

print("파일 전송이 완료되었습니다.")