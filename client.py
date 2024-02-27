import socket
import threading

IP = "127.0.0.1"
PORT = 8081


def main():
    client = create_socket()

    if client != 1:
        print("client socket created successfully")
        nickname = get_nickname()

        threading.Thread(target=send_data, args=(client,nickname)).start()
        threading.Thread(target=recv_data, args=(client,)).start()
    else:
        print("client failed!")
        return -1


def get_nickname():

    while True:
        nickname = input("enter your nickname: ")

        if len(nickname) > 20:
            print("Max nickname characters is 20")
        elif nickname.isdigit():
            print("Nickname must contain letters")
        elif nickname.isspace():
            print("Nickname can not contain space")
        else:
            break

    return nickname


def create_socket():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IP, PORT))

    except Exception as e:
        print(str(e))
        return -1

    return client


def send_data(client, nickname):
    try:
        client.send(str(nickname).encode())
    except Exception as e:
        print("error while sending nickname to server: "+ str(e))
    while True:
        msg = input()
        client.send(msg.encode())


def recv_data(client):

    while True:
        msg = client.recv(1024)
        print(f"{msg.decode('utf-8')}" )


if __name__ == '__main__':
    main()
