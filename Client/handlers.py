from client_socket import connect_and_send_wav_file


def recording_ended_handler(wav_path: str) -> str:
    recording_content = connect_and_send_wav_file(wav_path)
    return recording_content
