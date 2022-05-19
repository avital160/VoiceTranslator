import logging

import sounddevice
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
