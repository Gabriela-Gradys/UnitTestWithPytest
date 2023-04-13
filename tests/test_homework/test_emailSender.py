"""Test homework example solution.

Disclaimer: The solution can be a little different from yours, and it will be okay! :)
"""


import pytest
from homework.emailSender import EmailSender, AttachementError

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
