import socket
import os

server_address = ('192.168.50.60', 5555)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_address)

print(f"서버가 {server_address}에서 대기 중입니다...")

while True:
    data, client_address = server_socket.recvfrom(1024)
    filename = data.decode('utf-8')
    file_size, client_address = server_socket.recvfrom(1024)
    file_size = int(file_size.decode('utf-8'))
    print(f"파일 수신을 시작합니다. 파일 이름: {filename}, 파일 크기: {file_size} bytes")
    with open(filename, 'wb') as file:
        received_data_size = 0
        while received_data_size < file_size:
            data, client_address = server_socket.recvfrom(1024)
            file.write(data)
            received_data_size += len(data)
    print("파일 수신이 완료되었습니다.")