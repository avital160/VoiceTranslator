import Email_Sender
import Recorder
import Translator
from logger import Logger
from opencamera import EmailUtils


# from  tkinter import *


def main():
    log_helper = Logger()

    # secs = int(input('Enter time duration in seconds: '))
    # Recorder.record(secs)
    path = r'../out.wav'
    # txt = Recorder.voice_to_text(path).lower()
    txt = "send hi to kate in hebrew file hi"
    print(f'Original: {txt}')
    if txt:
        pharses = txt.split()
        if len(pharses) <= 7:
            print('Bad Format')
            return
        _1, *msg, _2, name, _3, language, _4, file_name = pharses
        print(msg)
        msg = ' '.join(msg)
        if (_1, _2, _3, _4) != ('send', 'to', 'in', 'file'):
            print('Bad Format')
            return
        file_name += '.jpg'
        # print(file_name)
        send_email = EmailUtils('Message from VoiceTranslator', name, msg, file_name, Email_Sender.contacts)
        send_email.send_email_with_attachment()
        translated = Translator.translate(msg, language)
        # Email_Sender.send_email(name, msg, language, translated)


if __name__ == '__main__':
    main()
