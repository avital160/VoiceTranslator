import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import secrets


class EmailUtils:

    def __init__(self, mail_content, receiver_address, email_subject, attach_file_name, emails_dictionary):
        self.mail_content = mail_content
        self.email_subject = email_subject
        self.attach_file_name = attach_file_name
        self.emails_dictionary = emails_dictionary
        self.receiver_address = self.emails_dictionary[receiver_address]

    def send_email_with_attachment(self):
        print("send_email_with_attachment")
        """This method send an email with attachment via gmail smtp"""
        # mail_content = '''Hello,
        # This is a test mail.
        # In this mail we are sending some attachments.
        # The mail is sent using Python SMTP library.
        # Thank You
        # '''
        # The mail addresses and password
        sender_address = secrets.EMAIL_ADDRESS
        sender_pass = secrets.EMAIL_PASSWORD
        receiver_address = secrets.TEST_RECEIVER_ADDRESS
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = self.receiver_address
        # message['Subject'] = 'A test mail sent by Python. It has an attachment.'
        message['Subject'] = self.email_subject
        # The subject line
        # The body and the attachments for the mail
        message.attach(MIMEText(self.mail_content, 'plain'))
        # attach_file_name = 'aaa.jpg'
        attach_file = open(self.attach_file_name, 'rb')  # Open the file as binary mode
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload)  # encode the attachment
        # add payload header with filename
        payload.add_header('Content-Decomposition', 'attachment', filename=self.attach_file_name)
        message.attach(payload)
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()

        session.sendmail(sender_address, self.receiver_address, text)
        session.quit()
        print('Mail Sent')
