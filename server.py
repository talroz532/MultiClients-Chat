from socket import *
import threading

IP = "127.0.0.1"
PORT = 8081


def main():
    clients = []

    server = create_server()

    if server != -1:
        print("[+] server created successfully ")
        threading.Thread(target=add_client, args=(server, clients,)).start()
        threading.Thread(target=recv_data, args=(clients, )).start()
        threading.Thread(target=send_data, args=(clients,)).start()

    else:
        print("server failed!")
        return -1


def create_server():
    try:
        server = socket(AF_INET, SOCK_STREAM)
        server.bind((IP, PORT))
        server.listen(5)

    except Exception as e:
        print(str(e))
        return -1

    return server


def add_client(server, clients):

    while True:
        try:
            conn, addr = server.accept()
            nickname = conn.recv(1024).decode('utf-8')
            clients.append((conn, addr, nickname))
            print(f"new connection from {str(addr)} {nickname}" )

        except Exception as e:
            print(f"Error accepting connection: {e}")


def send_data(clients):
    while True:
        msg = input()
        menu(msg, clients)
        for client in clients:
            conn, addr, _ = client
            conn.send(msg.encode())


def recv_data(clients):
    while True:
        for client in clients:
            conn, addr, nickname = client
            try:
                # Set the socket to non-blocking mode
                conn.setblocking(0)

                # Attempt to receive data
                msg = conn.recv(1024).decode('utf-8')

                if msg:
                    broadcasting(clients,msg, client)
                    print(f"{addr} [{nickname}] {msg}")

            except BlockingIOError:
                # No data available on the socket, continue to the next client
                pass
            except ConnectionResetError:
                # Connection forcibly closed by the remote host (client exited)
                print(f"Connection closed by {addr} [{nickname}]")
                # Broadcast a message to inform other clients about the disconnection
                broadcasting(clients, f"{nickname} has left the chat.", client)
                # Remove the disconnected client from the list
                clients.remove(client)
                conn.close()

            except Exception as e:
                print(f"Error receiving data from {addr}: {e}")


def broadcasting(clients, msg, off_client = None):
    _, _, nickname = off_client
    for client in clients:
        conn, addr, _ = client

        if off_client != client or off_client is None:
            msg = f"[{nickname}] {msg}"
            conn.send(msg.encode())


def menu(msg: str, clients):
    kick_spliter = msg.split()

    if msg == "!help":
        print("!list - listing all running clients \n!kick {nickname} - kick specific client \n"
              "!exit - close all clients ")

    elif kick_spliter[0] == "!kick":
        print("kick")

        for client in clients:
            conn, addr, nickname = client

            if nickname == kick_spliter[1]:
                try:
                    conn.close()
                    clients.remove(client)
                    kick_msg = f"{nickname} has been kicked! "
                    print(kick_msg)
                    broadcasting(clients, kick_msg)

                except Exception as e:
                    print(f"Error closing client socket: {e}")

    elif msg == "!exit":
        print("exit")

    elif msg == "!list":
        print("listing all the clients: ")
        print("\n\t ADDRESS \t\t NICKNAME \n")
        for client in clients:
            conn, addr, nickname = client
            print(f"{str(addr)} \t {nickname}")

    else:
        pass

if __name__ == '__main__':
    main()
