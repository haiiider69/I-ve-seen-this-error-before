"""Wait for a reply from a peer over a socket pair."""

import socket


def wait_for_reply(connection):
    connection.settimeout(0.2)
    return connection.recv(16)


def main():
    client, server = socket.socketpair()
    try:
        client.sendall(b"ping")
        server.sendall(b"pong")
        print(wait_for_reply(client))
    finally:
        client.close()
        server.close()


if __name__ == "__main__":
    main()
