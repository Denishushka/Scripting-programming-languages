import socket

def start_tcp_client(address=('127.0.0.1', 65433), msg='Привет!'):
    cl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with cl_socket:
        cl_socket.connect(address)
        cl_socket.sendall(msg.encode())
        response = cl_socket.recv(1024)
        print(f"Ответ сервера: {response.decode()}")

if __name__ == "__main__":
    start_tcp_client()
