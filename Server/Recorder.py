import logging

import sounddevice
import speech_recognition as sr
from scipy.io.wavfile import write

logger = logging.getLogger(__name__)


def record(seconds: int) -> None:
    fs = 44100
    logger.debug('Recording.....')
    sounddevice.default.dtype = 'int32', 'int32'
    record_voice = sounddevice.rec(int(seconds * fs), samplerate=fs, channels=2)
    sounddevice.wait()
    write('../out.wav', fs, record_voice)
    logger.debug('Recording finished')


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
