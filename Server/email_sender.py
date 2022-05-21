import logging
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from secrets import EMAIL_USERNAME, EMAIL_ADDRESS, EMAIL_PASSWORD, EXAMPLE_CONTACTS

contacts = EXAMPLE_CONTACTS

logger = logging.getLogger(__name__)


def create_mail(receiver_address: str, subject: str, body: str, file_attachment_path: str = '') -> str:
    try:
        mail_content = MIMEMultipart()
        mail_content['Subject'] = subject
        mail_content['From'] = EMAIL_ADDRESS
        mail_content['To'] = receiver_address

        mail_content.attach(MIMEText(body))

        part = MIMEBase('application', "octet-stream")
        if file_attachment_path:
            with open(file_attachment_path, 'rb') as file:
                part.set_payload(file.read())
                encoders.encode_base64(part)

                part.add_header('Content-Disposition', f'attachment; filename={Path(file_attachment_path).name}')
        mail_content.attach(part)

        logger.debug('mail created')

        return mail_content.as_string()
    except Exception as ex:
        logging.exception(f'{ex}')


def send_email(subject: str, body: str, contact: str, msg: str, lang: str, translated: str) -> None:
    receiver_address = contacts.get(contact, '')
    print("receiver_address: " + receiver_address)
    if not receiver_address:
        logger.info(f'{receiver_address} was not found in contacts')
        return

    mail_content = create_mail(subject, body, receiver_address, msg)  # Create SMTP body
    if not mail_content:
        return

    # Send through SMTP Gmail server
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Connect SMTP Server
    server.ehlo()
    server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, receiver_address, mail_content)
    server.close()

    logger.debug('email sent')
