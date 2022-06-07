from secrets import SENDER
from audio_actions import voice_to_text
from mail_format import Mail, MessageMail, TranslatedMessageMail, SharedMessageMail, FileMail, SharedFileMail
from email_sender import send_email


def wav_file_handler(wav_path: str) -> str:
    text_from_voice = voice_to_text(wav_path)
    sender = SENDER
    mail_obj = mail_object_from_plain_text(sender, text_from_voice)
    if mail_obj:
        send_email(mail_obj)
        return text_from_voice
    else:
        return '***Your message is not in right format***'


def mail_object_from_plain_text(sender: str, text: str) -> Mail:
    if text:
        args = (sender, text)
        return MessageMail.get_correct_object(*args) or \
               TranslatedMessageMail.get_correct_object(*args) or \
               SharedMessageMail.get_correct_object(*args) or \
               FileMail.get_correct_object(*args) or \
               SharedFileMail.get_correct_object(*args)

