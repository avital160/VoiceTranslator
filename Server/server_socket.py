import logging
import socket
import threading

import secrets
from utils import generate_random_filename

logger = logging.getLogger(__name__)

SERVER_ADDRESS = secrets.SERVER_ADDRESS
PORT = secrets.SERVER_PORT


def start_server() -> None:
    server_socket = None
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((SERVER_ADDRESS, PORT))
        server_socket.listen(5)
        while True:
            client_socket, address = server_socket.accept()
            threading.Thread(target=conn_with_client, args=[client_socket]).start()

    except:
        if server_socket:
            server_socket.close()


def conn_with_client(client_socket: socket.socket) -> None:
    try:
        length = client_socket.recv(8)
        length = int(length.decode())
        data = client_socket.recv(length)

        wav_path = generate_random_filename('wav')

        with open(wav_path, 'wb') as wav_file:
            wav_file.write(data)

    except Exception as ex:
        logger.exception(f'{ex}')
        if client_socket:
            client_socket.close()
