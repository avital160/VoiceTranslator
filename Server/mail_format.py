from abc import ABC, abstractmethod


class Mail(ABC):
    sender: str
    contacts: tuple
    with_date: bool
    with_file: bool

    def __init__(self, sender: str, contacts: tuple, with_date: bool) -> None:
        self.sender = sender
        self.contacts = contacts
        self.with_date = with_date
        self.with_file = False

    def __str__(self):
        return f'{self.sender=} {self.contacts=} {self.with_date=}'

    @abstractmethod
    def get_mail_subject(self):
        raise NotImplementedError

    @abstractmethod
    def get_mail_body(self):
        raise NotImplementedError


class FileMail(Mail):
    file_path: str

    def __init__(self, sender: str, contacts: tuple, with_date: bool, file_path: str) -> None:
        super().__init__(sender, contacts, with_date)
        self.with_file = True
        self.file_path = file_path

    def __str__(self):
        return f'{self.sender=} {self.contacts=} {self.with_date=} {self.file_path=}'

    def get_mail_subject(self):
        pass

    def get_mail_body(self):
        pass


class MessageMail(Mail):
    message: str

    def __init__(self, sender: str, contacts: tuple, with_date: bool, message: str) -> None:
        super().__init__(sender, contacts, with_date)
        self.message = message

    def __str__(self):
        return f'{self.sender=} {self.contacts=} {self.with_date=} {self.message=}'

    def get_mail_subject(self):
        pass

    def get_mail_body(self):
        pass


class TranslatedMessageMail(MessageMail):
    translation_language: str

    def __init__(self, sender: str, contacts: tuple, with_date: bool, message: str, translation_language: str) -> None:
        super().__init__(sender, contacts, with_date, message)
        self.translation_language = translation_language

    def __str__(self):
        return f'{self.sender=} {self.contacts=} {self.with_date=} {self.message=} {self.translation_language}'


class SharedMessageMail(MessageMail):
    def __init__(self, sender: str, with_date: bool, message: str) -> None:
        # TODO get all contracts method
        all_contracts = ()
        super().__init__(sender, all_contracts, with_date, message)
