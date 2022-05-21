import logging
import os
import socket

from secrets import SERVER_ADDRESS, SERVER_PORT

logger = logging.getLogger(__name__)


def connect() -> socket.socket:
    client_socket = None
    try:
        client_socket = socket.socket()
        client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
        logger.debug(f'connected successfully {client_socket=}')
        return client_socket
    except Exception as ex:
        logger.exception(f'failed to connect to the server {ex=}')
        if client_socket:
            client_socket.close()


def send_file_via_socket(client_socket: socket.socket, file_path: str, remove_file_after_sending: bool = True) -> str:
    try:
        with open(file_path, 'rb') as wav_file:
            data = wav_file.read()

        if remove_file_after_sending:
            os.remove(file_path)

        length = (str(len(data))).zfill(8)
        client_socket.send(length.encode())

        client_socket.send(data)

        logger.debug(f'{file_path=} sent')

        length = client_socket.recv(4)
        length = int(length.decode())
        recording_content = client_socket.recv(length).decode()
        return recording_content
    except Exception as ex:
        logger.exception(f'{ex}')


def connect_and_send_wav_file(wav_path: str) -> str:
    client_socket = connect()
    if client_socket:
        recording_content = send_file_via_socket(client_socket, wav_path)
        return recording_content
    logger.info('client_socket is None')
