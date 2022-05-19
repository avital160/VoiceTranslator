import smtplib
from email.mime.text import MIMEText
import traceback

import secrets

voice_emails = {}
USERNAME = secrets.EMAIL_USERNAME
ADDRESS = secrets.EMAIL_ADDRESS
PASSWORD = secrets.EMAIL_PASSWORD
SUBJECT = 'Voice Translator New Message!'
BODY = 'Message Received: {}\n' \
       'Translation in {}: {}'
contacts = secrets.EXAMPLE_CONTACTS


def create_mail(receiver_address: str, msg: str, language: str, translated: str) -> str:
    try:
        my_body = BODY.format(msg, language.capitalize(), translated)
        msg = MIMEText(my_body)
        msg['Subject'] = SUBJECT
        msg['From'] = ADDRESS
        msg['To'] = receiver_address
        msg = msg.as_string()
        return msg
    except Exception as e:
        print("Exception inside create_email")
        traceback.print_exc()
        return ''


def send_email(contact: str, msg: str, language: str, translated: str) -> None:
    receiver_address = contacts.get(contact, '')
    print("receiver_address: " + receiver_address)
    if not receiver_address:
        return
    msg = create_mail(receiver_address, msg, language, translated)  # Create SMTP body
    if not msg:
        print('Error occurred')
        return
    # Send through SMTP Gmail server
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Connect SMTP Server
    server.ehlo()
    server.login(USERNAME, PASSWORD)
    server.sendmail(ADDRESS, receiver_address, msg)
    server.close()
