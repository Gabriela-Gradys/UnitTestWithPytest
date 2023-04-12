import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
import smtplib


class ReportFileError(Exception):
    """Raised when a report file is missing or is corrupted"""
    pass


class EmailSender:
    """Class used to initialize email user and coordinate email distribution.

    :method _start_login_session: creates SMTP session with provided credentials
    :method _create_email: creates email body and attaches file if provided
    :method send_message: sends email as html email. Can attach file
    """

    def __init__(
            self,
            subject: str,
            to_email: str,
            cc_emails: [str],
            email_message: str = None,
    ):
        """Initializes email sender object.

        :param subject: subject of the email
        :param to_email: email reciver adress
        :param cc_emails: list of emails to be sent as CC
        :param email_message: message to be sent in the email, optional
        """

        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.smtp_host = "smtp.office365.com"
        self.smtp_PORT = 587

        self.subject = subject
        self.to_email = to_email
        self.cc_emails = ','.join(cc_emails)

        if email_message:
            self.email_message = email_message
        else:
            with open(os.getenv("EMAIL_TEMPLATE_PATH"), 'r') as template_file:
                self.email_message = template_file.read()

        self.session = self._start_login_session()

    def _start_login_session(self):
        """Creates email session with provided credentials

        :return: SMTP logged-in session"""

        session = smtplib.SMTP(self.smtp_host, self.smtp_PORT, timeout=5000)
        session.starttls()  # enable security
        session.login(self.sender_email, self.sender_password)

        return session

    def _create_email(self, file_name: str = None):
        """Creating email body and attaches file if provided.

        :param file_name: name of report .xlsx file
        :return: email as string
        """

        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['Subject'] = self.subject
        message['CC'] = self.cc_emails
        message['To'] = self.to_email

        message.attach(MIMEText(self.email_message, 'plain'))

        if file_name:
            reports_path = os.path.join(os.getenv("REPORT_PATH"), file_name)
            with open(reports_path, 'rb') as attachment:
                header_charset = 'ISO-8859-2'
                f_name = os.path.basename(file_name)
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                part.add_header('Content-Disposition',
                                "attachment",
                                filename=(str(Header(f_name, header_charset))))
                encoders.encode_base64(part)
                message.attach(part)

        return message.as_string()

    def send_message(self, file_name: str = None):
        """Sends email as html email. Can attach file.

        :param file_name: name of the file to be attached
        """

        self.session.sendmail(
            self.sender_email,
            self.to_email + self.cc_emails,
            self._create_email(file_name=file_name)
        )

    def __del__(self):
        """Log out and close session"""

        self.session.quit()
