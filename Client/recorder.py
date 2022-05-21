import logging
from multiprocessing import Queue

import sounddevice as sd
import soundfile as sf

from utils import generate_random_filename

logger = logging.getLogger(__name__)


def record(queue: Queue) -> None:
    wav_path = generate_random_filename(extension='wav')
    fs = 44100
    with sf.SoundFile(wav_path, mode='w', samplerate=fs, channels=2, subtype=None) as sound_file:
        with sd.InputStream(fs, channels=2) as input_stream:
            logger.debug('recording.....')
            while queue.empty():
                data, overflowed = input_stream.read(fs)
                sound_file.write(data)
            queue.get()  # release False in queue
    logger.debug('recording finished')
    queue.put(wav_path)
