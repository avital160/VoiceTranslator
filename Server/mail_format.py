import datetime
from abc import ABC, abstractmethod
from secrets import APP_CONTACTS


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
    def get_mail_subject(self):
        raise NotImplementedError

    @abstractmethod
    def get_mail_body(self):
        raise NotImplementedError

    def get_date_str_for_mail(self):
        if self.with_date:
            return f'Date: {datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}\n'
        else:
            return ''


class FileMail(Mail):
    file_path: str

    def __init__(self, sender: str, contacts: tuple, with_date: bool, file_path: str) -> None:
        super().__init__(sender, contacts, with_date)
        self.file_path = file_path

    def __str__(self):
        return f'{self.sender=} {self.contacts=} {self.with_date=} {self.file_path=}'

    def get_mail_subject(self):
        return f'{self.sender} sent you a file via VoiceTranslator!'

    def get_mail_body(self):
        return self.get_date_str_for_mail()


class MessageMail(Mail):
    message: str

    def __init__(self, sender: str, contacts: tuple, with_date: bool, message: str) -> None:
        super().__init__(sender, contacts, with_date)
        self.message = message

    def __str__(self):
        return f'{self.sender=} {self.contacts=} {self.with_date=} {self.message=}'

    def get_mail_subject(self):
        return f'{self.sender} sent you a message via VoiceTranslator!'

    def get_mail_body(self):
        return f'{self.get_date_str_for_mail()}' \
               f'{self.message}'


class TranslatedMessageMail(MessageMail):
    translated_message: str

    def __init__(self, sender: str, contacts: tuple, with_date: bool, message: str, translated_message: str) -> None:
        super().__init__(sender, contacts, with_date, message)
        self.translated_message = translated_message

    def __str__(self):
        return f'{self.sender=} {self.contacts=} {self.with_date=} {self.message=} {self.translated_message}'

    def get_mail_subject(self):
        return f'{self.sender} sent you a translated message via VoiceTranslator!'

    def get_mail_body(self):
        return f'{self.get_date_str_for_mail()}' \
               f'Original Message: {self.message}\n' \
               f'Translated Message: {self.translated_message}'


class SharedMessageMail(MessageMail):
    def __init__(self, sender: str, with_date: bool, message: str) -> None:
        all_contracts = APP_CONTACTS
        super().__init__(sender, all_contracts, with_date, message)

    def get_mail_subject(self):
        return f'{self.sender} sent a message to everyone via VoiceTranslator!'
