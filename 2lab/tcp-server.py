import socket

def start_tcp_server(address=('127.0.0.1', 65433)):
    #Создаёт сокет
    srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with srv_socket:
        #Привязывает сокет к адресу и порту
        srv_socket.bind(address)
        #Слушает входящие подключения
        srv_socket.listen()
        print(f"Сервер активен по адресу {address[0]}:{address[1]}")
        
        connection, client_addr = srv_socket.accept()
        with connection:
            print(f"Подключён клиент: {client_addr}")
            received_data = connection.recv(1024)
            if received_data:
                print(f"Получено сообщение: {received_data.decode()}")
                connection.sendall(received_data)
                print("Эхо-сообщение отправлено клиенту")

if __name__ == "__main__":
    start_tcp_server()
