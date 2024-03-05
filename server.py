from socket import *
import threading, time

IP = "127.0.0.1"
PORT = 8081


def main():
    exit_event = threading.Event()  # Event to signal threads to exit
    clients = [] #list of all clients
    server = create_server() 

    if server != -1:
        print("[+] server created successfully ")
        add_client_thread = threading.Thread(target=add_client, args=(server, clients, exit_event))
        recv_thread = threading.Thread(target=recv_data, args=(clients, exit_event))
        send_thread = threading.Thread(target=send_data, args=(clients, exit_event))

        add_client_thread.start()
        recv_thread.start()
        send_thread.start()

        exit_program(add_client_thread,recv_thread,send_thread,server,clients)

    else:
        print("server failed!")
        return -1

# setup server
def create_server():
    try:
        server = socket(AF_INET, SOCK_STREAM)
        server.bind((IP, PORT))
        server.listen(5)

    except Exception as e:
        print(str(e))
        return -1

    return server

# function to add client when client is tring to connect
def add_client(server, clients, exit_event):
    server.settimeout(1)  # Set a timeout on server.accept()

    while not exit_event.is_set():
        try:
            conn, addr = server.accept()
            nickname = conn.recv(1024).decode('utf-8')
            clients.append((conn, addr, nickname))
            print(f"new connection from {str(addr)} {nickname}")
        except timeout:
            pass
        except Exception as e:
            print(f"Error accepting connection: {e}")


# function to send data to all clients
def send_data(clients, exit_event):
    while not exit_event.is_set():  # Check exit_event before continuing
        msg = input()
        if menu(msg, clients, exit_event) == 0:
            msg = "[SERVER] " + msg
            for client in clients:
                conn, addr, _ = client
                try:
                    conn.send(msg.encode())
                except Exception as e:
                    print(f"Error sending data to {addr}: {e}")


# function to receive data from clients
def recv_data(clients, exit_event):
    while not exit_event.is_set():  # Check exit_event before continuing
        for client in clients:
            conn, addr, nickname = client
            try:
                conn.setblocking(0)
                msg = conn.recv(1024).decode('utf-8')
                if msg:
                    broadcasting(clients, msg, client)
                    print(f"{addr} [{nickname}] {msg}")

            except BlockingIOError:
                pass
            except ConnectionResetError:
                print(f"Connection closed by {addr} [{nickname}]")
                broadcasting(clients, f"{nickname} has left the chat.", client)
                clients.remove(client)
                conn.close()
                break

            except Exception as e:
                print(f"Error receiving data from {addr}: {e}")
        time.sleep(0.1)


# function to send data to all clients, except off_client
def broadcasting(clients, msg, off_client=None):
    _, _, nickname = off_client

    for client in clients:
        conn, addr, _ = client

        if off_client != client or off_client is None:
            try:
                msg_to_send = f"[{nickname}] fgh {msg}"
                conn.send(msg_to_send.encode())

            except Exception as e:
                print(f"Error broadcasting to {addr}: {e}")


# menu to check for commands from the server
def menu(msg: str, clients, exit_event):
    kick_spliter = msg.split()

    if msg == "!help":
        print("!list - listing all running clients \n!kick {nickname} - kick specific client \n"
              "!exit - close all clients ")

    elif kick_spliter and kick_spliter[0] == "!kick":  # Check if kick_spliter is not empty
        print("kick")

        for client in clients:
            conn, addr, nickname = client

            if len(kick_spliter) > 1 and nickname == kick_spliter[1]:  # Check if there's a nickname provided
                try:
                    conn.close()
                    clients.remove(client)

                    kick_msg = f"{nickname} has been kicked! "
                    print(kick_msg)
                    broadcasting(clients, kick_msg, client)

                except Exception as e:
                    print(f"Error closing client socket: {e}")

    elif msg == "!exit":
        print("exitMENU")
        exit_event.set()  # Set the exit_event to signal threads to exit
        return 1  # Indicate that the program should exit

    elif msg == "!list":
        print("listing all the clients: ")
        print("\n\t ADDRESS \t\t NICKNAME \n")
        for client in clients:
            conn, addr, nickname = client
            print(f"{str(addr)} \t {nickname}")

    else:
        return 0

# function to end all threads, clear clients list, close open sockets
def exit_program(add_client_thread, recv_thread, send_thread, server, clients):

    add_client_thread.join()
    recv_thread.join()
    send_thread.join()

    for client in clients:
        conn, addr, _ = client
        conn.close()

    clients.clear()
    server.close()
    print("[+] server has been closed!")


if __name__ == '__main__':
    main()
