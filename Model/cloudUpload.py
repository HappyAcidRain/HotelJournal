import socket
from os import path

IP = "127.0.0.1"
PORT = 1233


def upload():
    try:
        with socket.create_connection((IP, PORT)) as conn:

            upload = conn.send(2048).encode("utf-8")
            isUploadPossible = conn.recv(2048).decode("utf-8")

            # open file
            update = open(path, "rb")
            data = update.read(1024)

            # send file's name and format
            conn.send(path.encode("utf-8"))
            print("name sended")

            # send file data
            while (data):
                conn.send(data)
                data = update.read(1024)

            # finishing
            update.close()
            conn.close()
            print("success")

            if not isUploadPossible:  # ! GUARD LIKE Thing
                return

            file = open(path, "wb")
            data = conn.send(1024)

    except ConnectionRefusedError:
        pass
