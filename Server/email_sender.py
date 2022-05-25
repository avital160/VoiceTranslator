import logging
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from Server.mail_format import Mail
from secrets import EMAIL_USERNAME, EMAIL_ADDRESS, EMAIL_PASSWORD, APP_CONTACTS

logger = logging.getLogger(__name__)


def create_mail(mail_obj: Mail) -> str:
    try:
        logger.debug(f'starting create mail with obj type {type(mail_obj)}: {mail_obj}')

        mail_content = MIMEMultipart()
        mail_content['Subject'] = mail_obj.get_mail_subject()
        mail_content['From'] = EMAIL_ADDRESS
        mail_content['To'] = ', '.join([APP_CONTACTS.get(contact,"") for contact in mail_obj.contacts])

        mail_content.attach(MIMEText(mail_obj.get_mail_body()))

        part = MIMEBase('application', "octet-stream")
        if hasattr(mail_obj, 'file_path'):
            with open(mail_obj.file_path, 'rb') as file:
                part.set_payload(file.read())
                encoders.encode_base64(part)

                part.add_header('Content-Disposition', f'attachment; filename={Path(mail_obj.file_path).name}')
        mail_content.attach(part)

        logger.debug('mail created')

        return mail_content.as_string()
    except Exception as ex:
        logging.exception(f'{ex}')


def send_email(mail_obj: Mail) -> None:
    for contact in mail_obj.contacts:
        if contact not in APP_CONTACTS:
            logger.info(f'{contact} was not found in contacts')
            return

    mail_content = create_mail(mail_obj)  # Create SMTP body
    if not mail_content:
        return

    # Send through SMTP Gmail server
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Connect SMTP Server
    server.ehlo()
    server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS,[APP_CONTACTS.get(contact,"") for contact in mail_obj.contacts], mail_content)
    server.close()

    logger.debug('email sent')
