import socket, threading, sys

IP = "127.0.0.1"
PORT = 8081


def main():
    exit_event = threading.Event()
    client = create_socket(exit_event)

    if client:
        print("Client socket created successfully")
        nickname = get_nickname()

        send_thread = threading.Thread(target=send_data, args=(client, nickname, exit_event))
        recv_thread = threading.Thread(target=recv_data, args=(client, exit_event))

        send_thread.start()
        recv_thread.start()

        exit_program(send_thread, recv_thread, client)

    else:
        print("Client failed!")


# function to create set up client socket
def create_socket(exit_event):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IP, PORT))
        return client
    except (socket.error, OSError) as e:
        print(f"Error creating socket: {e}")
        exit_event.set()
        return None


# function to send data to all clients
def send_data(client, nickname, exit_event):
    try:
        client.send(str(nickname).encode())
    except socket.error as e:
        print(f"Error sending nickname to server: {e}")

    while not exit_event.is_set():
        msg = input()
        if msg == "!exit":
            exit_event.set()
            break

        if msg.strip():
            try:
                client.send(msg.encode())
            except socket.error as e:
                print(f"Error sending message: {e}")

    client.close()


# function to receive data from clients
def recv_data(client, exit_event):
    while not exit_event.is_set():
        try:
            msg = client.recv(1024)
            if not msg:
                # If no data is received, the connection might be closed
                print("Connection closed by the server. ")
                exit_event.set()
                break
            print(msg.decode('utf-8'))
        except Exception as e:
            if not exit_event.is_set():
                print(f"Error receiving message: {e}")
                exit_event.set()
                break


# function to get the nickname of the client
def get_nickname():
    while True:
        nickname = input("Enter your nickname: ")

        if len(nickname) > 20:
            print("Max nickname characters is 20")
        elif nickname.isdigit():
            print("Nickname must contain letters")
        elif ' ' in nickname:
            print("Nickname cannot contain space")
        else:
            break

    return nickname


# function to end all threads, clear clients list, close open socket
def exit_program(send_thread, recv_thread, client):
    send_thread.join()
    recv_thread.join()

    client.close()
    sys.exit()


if __name__ == '__main__':
    main()
