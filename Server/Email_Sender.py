import logging
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import secrets

voice_emails = {}
USERNAME = secrets.EMAIL_USERNAME
ADDRESS = secrets.EMAIL_ADDRESS
PASSWORD = secrets.EMAIL_PASSWORD
SUBJECT = 'Voice Translator New Message!'
BODY = 'Message Received: {}\n' \
       'Translation in {}: {}'
contacts = secrets.EXAMPLE_CONTACTS

logger = logging.getLogger(__name__)


def create_mail(receiver_address: str, msg: str, lang: str, translated: str, file_attachment_path: str = None) -> str:
    try:
        my_body = BODY.format(msg, lang.capitalize(), translated)

        mail_content = MIMEMultipart()
        mail_content['Subject'] = SUBJECT
        mail_content['From'] = ADDRESS
        mail_content['To'] = receiver_address

        mail_content.attach(MIMEText(my_body))

        part = MIMEBase('application', "octet-stream")
        with open(file_attachment_path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        # payload.add_header('Content-Decomposition', 'attachment', filename=self.attach_file_name)

        part.add_header('Content-Disposition', 'attachment; filename={}'.format(Path(file_attachment_path).name))
        mail_content.attach(part)

        logger.debug('mail created')

        return mail_content.as_string()
    except Exception as ex:
        logging.exception(f'{ex}')


def send_email(contact: str, msg: str, lang: str, translated: str) -> None:
    receiver_address = contacts.get(contact, '')
    print("receiver_address: " + receiver_address)
    if not receiver_address:
        logger.info(f'{receiver_address} was not found in contacts')
        return

    mail_content = create_mail(receiver_address, msg, lang, translated)  # Create SMTP body
    if not mail_content:
        return

    # Send through SMTP Gmail server
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Connect SMTP Server
    server.ehlo()
    server.login(USERNAME, PASSWORD)
    server.sendmail(ADDRESS, receiver_address, mail_content)
    server.close()

    logger.debug('email sent')
