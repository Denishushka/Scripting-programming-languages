import socket

def start_udp_server(address=('127.0.0.1', 65432)):
    srv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with srv_socket:
        srv_socket.bind(address)
        print(f"UDP-сервер активен на {address[0]}:{address[1]}")
        
        while True:
            received_data, client_addr = srv_socket.recvfrom(1024)
            if received_data:
                print(f"Получено сообщение от {client_addr}: {received_data.decode()}")
                srv_socket.sendto(received_data, client_addr)
                print("Эхо-сообщение отправлено обратно клиенту")

if __name__ == "__main__":
    start_udp_server()
