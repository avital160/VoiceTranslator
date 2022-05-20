from abc import ABC, abstractmethod


class Mail(ABC):
    contacts: tuple = ()
    add_date: bool = False

    def __init__(self, contacts: tuple, add_date: bool) -> None:
        self.contacts = contacts
        self.add_date = add_date

    @abstractmethod
    def get_mail_subject(self):
        raise NotImplementedError

    @abstractmethod
    def get_mail_body(self):
        raise NotImplementedError


class FileMail(Mail):
    file_path: str = ''

    def __init__(self, contacts: tuple, add_date: bool, file_path: str) -> None:
        super().__init__(contacts, add_date)
        self.file_path = file_path

    def get_mail_subject(self):
        pass

    def get_mail_body(self):
        pass


class MessageMail(Mail):
    message: str = ''

    def __init__(self, contacts: tuple, add_date: bool, message: str) -> None:
        super().__init__(contacts, add_date)
        self.message = message

    def get_mail_subject(self):
        pass

    def get_mail_body(self):
        pass


class SharedMessageMail(MessageMail):
    def __init__(self, add_date: bool, message: str) -> None:
        # TODO get all contracts method
        all_contracts = ()
        super().__init__(all_contracts, add_date, message)