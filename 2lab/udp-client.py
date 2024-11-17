import socket

def start_udp_client(address=('127.0.0.1', 65432), msg='Привет!'):
    cl_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with cl_socket:
        cl_socket.sendto(msg.encode(), address)
        response, _ = cl_socket.recvfrom(1024)
        print(f"Ответ от сервера: {response.decode()}")

if __name__ == "__main__":
    start_udp_client()
