import datetime
from abc import ABC, abstractmethod
from Server.translator import translate_text
from secrets import APP_CONTACTS


# TODO get_correct_object should return the object of the current class and validate with check the correct format
class Mail(ABC):
    sender: str
    contacts: tuple
    with_date: bool

    def __init__(self, sender: str, contacts: tuple, with_date: bool) -> None:
        self.sender = sender
        self.contacts = contacts
        self.with_date = with_date

    def __str__(self):
        return f'{self.sender=} {self.contacts=} {self.with_date=}'

    @abstractmethod
    def get_mail_subject(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_mail_body(self) -> str:
        raise NotImplementedError

    def get_date_str_for_mail(self):
        if self.with_date:
            return f'Date: {datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}\n'
        else:
            return ''

    @staticmethod
    @abstractmethod
    def get_correct_object(sender: str, text: str):
        raise NotImplementedError


# send {message} to {contact} with date (optional)
class MessageMail(Mail):
    message: str

    def __init__(self, sender: str, contacts: tuple, with_date: bool, message: str) -> None:
        super().__init__(sender, contacts, with_date)
        self.message = message

    def __str__(self):
        return f'{self.sender=} {self.contacts=} {self.with_date=} {self.message=}'

    def get_mail_subject(self) -> str:
        return f'{self.sender} sent you a message via VoiceTranslator!'

    def get_mail_body(self) -> str:
        return f'{self.get_date_str_for_mail()}' \
               f'{self.message}'

    @staticmethod
    def get_correct_object(sender: str, text: str):
        try:
            assert text
            if text.endswith('with date'):
                send, *message, to, contact = text.split()[:-2]
                with_date = True
            else:
                send, *message, to, contact = text.split()
                with_date = False
            message = ' '.join(message)
            assert send == 'send'
            assert message
            assert to == 'to'
            assert contact
            contacts = (contact,)
            return MessageMail(sender, contacts, with_date, message)
        except:
            return None


# send {message} to {contact} in {language} with date (optional)
class TranslatedMessageMail(MessageMail):
    translated_message: str

    def __init__(self, sender: str, contacts: tuple, with_date: bool, message: str, translation_language: str) -> None:
        super().__init__(sender, contacts, with_date, message)
        self.translated_message = translate_text(self.message, translation_language)

    def __str__(self):
        return f'{self.sender=} {self.contacts=} {self.with_date=} {self.message=} {self.translated_message=}'

    def get_mail_subject(self) -> str:
        return f'{self.sender} sent you a translated message via VoiceTranslator!'

    def get_mail_body(self) -> str:
        return f'{self.get_date_str_for_mail()}' \
               f'Original Message: {self.message}\n' \
               f'Translated Message: {self.translated_message}'

    @staticmethod
    def get_correct_object(sender: str, text: str):
        #fixme here
        try:
            pass
        except:
            return None


# send {message} to everybody with date
class SharedMessageMail(MessageMail):
    def __init__(self, sender: str, with_date: bool, message: str) -> None:
        all_contracts = APP_CONTACTS
        super().__init__(sender, all_contracts, with_date, message)

    def get_mail_subject(self) -> str:
        return f'{self.sender} sent a message to everyone via VoiceTranslator!'

    @staticmethod
    def get_correct_object(sender: str, text: str):
        #fixme here
        try:
            pass
        except:
            return None


# send file {filename} to {contact} with date
class FileMail(Mail):
    file_path: str

    def __init__(self, sender: str, contacts: tuple, with_date: bool, file_path: str) -> None:
        super().__init__(sender, contacts, with_date)
        self.file_path = file_path

    def __str__(self):
        return f'{self.sender=} {self.contacts=} {self.with_date=} {self.file_path=}'

    def get_mail_subject(self) -> str:
        return f'{self.sender} sent you a file via VoiceTranslator!'

    def get_mail_body(self) -> str:
        return self.get_date_str_for_mail()

    @staticmethod
    def get_correct_object(sender: str, text: str):
        #fixme here
        try:
            pass
        except:
            return None


# send file {filename} to everybody with date
class SharedFileMail(FileMail):
    def __init__(self, sender: str, with_date: bool, file_path: str) -> None:
        all_contracts = APP_CONTACTS
        super().__init__(sender, all_contracts, with_date, file_path)

    def get_mail_subject(self) -> str:
        return f'{self.sender} sent a file to everyone via VoiceTranslator!'

    @staticmethod
    def get_correct_object(sender: str, text: str):
        #fixme here
        try:
            pass
        except:
            return None
