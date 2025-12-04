from socket import *
import threading

clients = []

def broadcast(data, exclude_socket=None):
    for client in clients:
        if client != exclude_socket:
            client.sendall(data)
            try:
                client.sendall(data)
            except:
                 #print("Тут сталась помилка")
                pass

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                break
            broadcast(data, exclude_socket=client_socket)
        except:
            break

        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()


def main():

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind(("localhost" , 12345))
    server_socket.setblocking(0)
    server_socket.listen(5)
    print(f"Сервер запущено на {'localhost'}:{12345}")


    while True:
        try:
            connection, address = server_socket.accept()
            print(f"Підключився клієнт , {address}")
            connection.setblocking(0)
            clients.append(connection)

            t = threading.Thread(target = handle_client, args=connection, )
            t.start()
        except:
            pass

if __name__ == "__main__":
    main()