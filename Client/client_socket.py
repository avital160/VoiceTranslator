import logging
import os
import socket

import secrets

logger = logging.getLogger(__name__)

SERVER_ADDRESS = secrets.SERVER_ADDRESS
PORT = secrets.SERVER_PORT


def connect() -> socket.socket:
    client_socket = None
    try:
        client_socket = socket.socket()
        client_socket.connect((SERVER_ADDRESS, PORT))
        logger.debug(f'connected successfully {client_socket=}')
        return client_socket
    except Exception as ex:
        logger.exception(f'failed to connect to the server {ex=}')
        if client_socket:
            client_socket.close()


def send_file_via_socket(client_socket: socket.socket, file_path: str, remove_file_after_sending: bool = True) -> None:
    try:
        with open(file_path, 'rb') as wav_file:
            data = wav_file.read()

        if remove_file_after_sending:
            os.remove(file_path)

        length = (str(len(data))).zfill(8)
        client_socket.send(length.encode())

        client_socket.send(data)

        logger.debug(f'{file_path=} sent')
    except Exception as ex:
        logger.exception(f'{ex}')


def connect_and_send_wav_file(wav_path: str):
    client_socket = connect()
    if not client_socket:
        logger.info('client_socket is None')
        return

    send_file_via_socket(client_socket, wav_path)
