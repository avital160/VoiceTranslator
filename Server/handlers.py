def wav_file_handler(wav_path: str) -> str:
    text_from_voice = voice_to_text(wav_path)
    print(text_from_voice)
    sender = SENDER
    mail_obj = mail_object_from_plain_text(sender, text_from_voice)
    send_email(mail_obj)
    return text_from_voice
