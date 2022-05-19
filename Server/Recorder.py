import sounddevice
import speech_recognition as sr
from scipy.io.wavfile import write

def record(seconds: int) -> None:
    fs = 44100
    print('Recording.....')
    sounddevice.default.dtype = 'int32', 'int32'
    record_voice = sounddevice.rec(int(seconds * fs), samplerate=fs, channels=2)
    sounddevice.wait()
    write('../out.wav', fs, record_voice)
    print('Finished.....Please check your output file')


def voice_to_text(voice_file_path: str) -> str:
    r = sr.Recognizer()
    audio_file = sr.AudioFile(voice_file_path)
    with audio_file as source:
        audio = r.record(source)
    try:
        s = r.recognize_google(audio)
        return s
    except:
        exception_msg = "error while trying to translate voice to tesxt from google"
        # log_helper.write_excetion_log(exception_msg)
        return exception_msg
