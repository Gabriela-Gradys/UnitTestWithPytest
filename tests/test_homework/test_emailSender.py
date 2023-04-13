"""Test homework example solution.

Disclaimer: The solution can be a little different from yours, and it will be okay! :)
"""


import pytest
from homework.emailSender import EmailSender, AttachementError


@pytest.fixture()
def mock_env_variables(monkeypatch, tmp_path):
    """Mock every environment variable"""

    template_path = tmp_path / "path.txt"
    template_path.write_text("Text message from template path")
    monkeypatch.setenv("EMAIL_TEMPLATE_PATH", str(template_path))
    monkeypatch.setenv("SENDER_EMAIL", "sender@email.com")
    monkeypatch.setenv("SENDER_PASSWORD", "secretPassword.!")


@pytest.fixture()
def mock_path_file_format(monkeypatch, tmp_path):
    """Mock environment variable with inappriopriate file extenstion.
    For testing: test_check_file_text_format"""

    template_path = tmp_path / "path.docx"
    monkeypatch.setenv("EMAIL_TEMPLATE_PATH", str(template_path))


@pytest.fixture()
def mock_login_session(mock_env_variables, monkeypatch, tmp_path):  # mock_env_variables
    """Create fixture instance of EmailSender."""

    class MockLoginSession:
        """Simulate _start_login_session.

        This is a replacement for self.session = self._start_login_session().
        Instead of creating external SMTP object, we only simulate it.
        """

        def __init__(self):
            pass

        def sendmail(self, *_, **__):  # args and kwargs
            """Simulate self.session.sendmail"""
            pass

        def quit(self, *_, **__):  # args and kwargs
            """Simulate self.session.quit()"""
            pass

    monkeypatch.setattr(
        "homework.emailSender.EmailSender._start_login_session", MockLoginSession
    )


@pytest.fixture()
def email_sender(mock_login_session, request):
    """Create EmailSender instance in fixture."""

    sender = EmailSender(
        subject="Subject Text",
        to_email="receiver@mail.com",
        cc_emails=["cc_receiver_1@mail.com", "cc_receiver_2@mail.com"],
    )
    return sender


@pytest.fixture()
def mime_multi_fixture(monkeypatch, tmp_path):
    """Mocks which are needed for testing _create_email() method.

    For the persistent! :)
    """

    class MockMimeMulti:
        """Mocked MimeMultipart.

        The class needs to contain every method which is called on 'message'
        variable in emailSender.py"""

        def __init__(self):
            self.mail = {}
            self.tested_text = []

        def __setitem__(self, key, value):
            self.mail[key] = value

        def __getitem__(self, item):
            return self.mail[item]

        def attach(self, message):
            """Simulate message.attach(MIMEText(self.email_message), 'plain')"""

            self.tested_text.append(message)
            return str(message)

        def as_string(self):
            """Simulate message.as_string"""

            return self.tested_text

    class MockMimeBase:
        """Mocked MimeBase class."""

        def __init__(self, apllication, octet_stream):
            self.application = apllication
            self.octet_stream = octet_stream

        def set_payload(self, attachement):
            """Simulate getting text from attachment."""

            assert b"Workshop testing!" in attachement

        def add_header(self, *_, **__):
            """Simulate adding header - part.add_header(...)"""
            return

    class MockHeader:
        """Mocked Header class."""

        def __init__(self, *_, **__):
            return

    class MockEncoders:
        """Simulate creating encode instance"""

        @staticmethod
        def encode_base64(*_, **__):
            """Simulate calling encode_base64(part)"""

            return

    def mock_mime_text(message, *_, **__):
        """Simulate MIMEText()"""

        return str(message)

    report_path = tmp_path
    file_name = tmp_path / "file_name.txt"
    file_name.write_text("Workshop testing!")

    monkeypatch.setattr("homework.emailSender.MIMEMultipart", MockMimeMulti)
    monkeypatch.setattr("homework.emailSender.MIMEBase", MockMimeBase)
    monkeypatch.setattr("homework.emailSender.Header", MockHeader)
    monkeypatch.setattr("homework.emailSender.MIMEText", mock_mime_text)
    monkeypatch.setattr("homework.emailSender.encoders", MockEncoders)
    monkeypatch.setenv("REPORT_PATH", str(report_path))


@pytest.mark.parametrize(
    "input_message, output",
    [
        ("Given text message", "Given text message"),
        (None, "Text message from template path"),
    ],
)
def test_create_email_sender_instance(input_message, output, mock_login_session):
    """Check if EmailSender object was created with every attribute."""

    parametrized_sender = EmailSender(
        subject="Subject Text",
        to_email="receiver@mail.com",
        cc_emails=["cc_receiver_1@mail.com", "cc_receiver_2@mail.com"],
        email_message=input_message,
    )

    assert isinstance(parametrized_sender, EmailSender)
    assert output in parametrized_sender.email_message
    assert (
        "cc_receiver_1@mail.com,cc_receiver_2@mail.com" in parametrized_sender.cc_emails
    )
    assert "sender@email.com" in parametrized_sender.sender_email


def test_check_file_text_format(mock_login_session, mock_path_file_format):
    """Check if EMAIL_TEMPLATE_PATH env has a proper format - .txt"""

    with pytest.raises(
        AttachementError, match="Email path env should lead to .txt file!"
    ):
        EmailSender(
            subject="Subject Text",
            to_email="receiver@mail.com",
            cc_emails=["cc_receiver_1@mail.com", "cc_receiver_2@mail.com"],
        )


def test_send_message(email_sender, capsys):
    """Check send_message"""

    email_sender.send_message()
    captured = capsys.readouterr()
    assert "Email had been sent from sender@email.com to " in captured.out


def test_create_email(mime_multi_fixture, email_sender, tmp_path):
    """Check create_email attachment.

    MIMEMultipart is not tested as it is an external library."""

    file_name = tmp_path / "file_name.txt"
    file_name.write_text("Workshop testing!")
    result = email_sender._create_email(file_name=str(file_name))
    assert "Text message from template path" in result
