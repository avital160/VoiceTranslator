import logging

import speech_recognition as sr

logger = logging.getLogger(__name__)


def voice_to_text(voice_file_path: str) -> str:
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(voice_file_path)
    try:
        with audio_file as source:
            logger.debug(f'{voice_file_path=} recording started')
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        return text
    except Exception as ex:
        logger.exception(f'{ex}')
