import logging

import sounddevice
from scipy.io.wavfile import write

from utils import generate_random_filename

logger = logging.getLogger(__name__)


def record(seconds: int) -> str:
    fs = 44100
    logger.debug('Recording.....')
    sounddevice.default.dtype = 'int32', 'int32'
    record_voice = sounddevice.rec(int(seconds * fs), samplerate=fs, channels=2)
    sounddevice.wait()
    wav_path = generate_random_filename(extension='wav')
    write(wav_path, fs, record_voice)
    logger.debug('Recording finished')
    return wav_path
