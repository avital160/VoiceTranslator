import logging
import os
import socket
import threading

from secrets import SERVER_ADDRESS, SERVER_PORT
from logger_config import config_server_logger
from handlers import wav_file_handler
from utils import generate_random_filename

config_server_logger()
logger = logging.getLogger(__name__)


def start_server() -> None:
    server_socket = None
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
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

        logger.debug(f'data received from {client_socket=}')

        wav_path = generate_random_filename('wav')

        with open(wav_path, 'wb') as wav_file:
            wav_file.write(data)

        logger.debug(f'wav file {wav_path} was written successfully')

        recording_content = wav_file_handler(wav_path)

        os.remove(wav_path)

        length = (str(len(recording_content))).zfill(4)
        client_socket.send(length.encode())

        client_socket.send(recording_content.encode())

    except Exception as ex:
        logger.exception(f'{ex}')
        if client_socket:
            client_socket.close()


def main():
    start_server()


if __name__ == '__main__':
    main()
