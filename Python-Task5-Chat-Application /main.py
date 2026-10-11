import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5555

clients = []
usernames = []


def get_time():
    return datetime.now().strftime("%H:%M")


def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.send(message.encode("utf-8"))
            except:
                remove_client(client)


def remove_client(client):
    if client in clients:
        index = clients.index(client)
        username = usernames[index]

        clients.remove(client)
        usernames.remove(username)

        client.close()

        message = f"[{get_time()}] {username} has left the chat."
        print(message)

        broadcast(message)


def handle_client(client):
    try:
        username = client.recv(1024).decode("utf-8")

        clients.append(client)
        usernames.append(username)

        join_message = f"[{get_time()}] {username} joined the chat."
        print(join_message)

        broadcast(join_message, client)

        while True:
            message = client.recv(1024).decode("utf-8")

            if not message:
                break

            full_message = f"[{get_time()}] {username}: {message}"

            print(full_message)
            broadcast(full_message, client)

    except:
        pass

    finally:
        remove_client(client)


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST, PORT))
    server.listen()

    print("===================================")
    print("       CHAT SERVER STARTED")
    print("===================================")
    print(f"Server running on {HOST}:{PORT}")
    print("Waiting for clients...\n")

    while True:
        client, address = server.accept()

        print(f"New connection from {address}")

        thread = threading.Thread(
            target=handle_client,
            args=(client,)
        )

        thread.start()


if __name__ == "__main__":
    start_server()
