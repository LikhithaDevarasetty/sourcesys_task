from __future__ import annotations

import os
from unittest.mock import MagicMock, patch
import pytest
import smtplib

from services.emailer import (
    send_email,
    send_login_email,
    send_logout_email,
    send_password_reset_email,
    send_reset_code_email,
)


@pytest.fixture()
def mock_env():
    """Mock environment variables for SMTP settings."""
    old_env = dict(os.environ)
    os.environ["SMTP_HOST"] = "smtp.myfinancedomain.org"
    os.environ["SMTP_PORT"] = "587"
    os.environ["SMTP_USERNAME"] = "testuser"
    os.environ["SMTP_PASSWORD"] = "testpass"
    os.environ["EMAIL_FROM"] = "no-reply@myfinancedomain.org"
    os.environ["SMTP_RETRIES"] = "2"
    os.environ["SMTP_BACKOFF_BASE"] = "0.01"  # Keep retries very fast in tests
    yield
    os.environ.clear()
    os.environ.update(old_env)


def test_send_email_skips_if_placeholder():
    """Verify that placeholder or empty environment variables prevent SMTP connections."""
    with patch("os.getenv") as mock_getenv:
        mock_getenv.side_effect = lambda key, default=None: {
            "SMTP_HOST": "YOUR_SMTP_HOST",
            "SMTP_PORT": "587",
            "SMTP_USERNAME": "test",
            "SMTP_PASSWORD": "password",
            "EMAIL_FROM": "sender@example.com",
        }.get(key, default)

        with patch("smtplib.SMTP") as mock_smtp:
            send_email("to@example.com", "Subject", "Body")
            mock_smtp.assert_not_called()


@patch("smtplib.SMTP")
def test_send_email_success(mock_smtp_class, mock_env):
    """Test successful email transmission through a mocked smtplib.SMTP context manager."""
    mock_smtp_instance = MagicMock()
    mock_smtp_class.return_value.__enter__.return_value = mock_smtp_instance

    send_email("to@myfinancedomain.org", "Subject Line", "Body content message.")

    mock_smtp_class.assert_called_once_with("smtp.myfinancedomain.org", 587, timeout=10)
    mock_smtp_instance.starttls.assert_called_once()
    mock_smtp_instance.login.assert_called_once_with("testuser", "testpass")
    mock_smtp_instance.send_message.assert_called_once()


@patch("smtplib.SMTP")
def test_send_email_retries_and_raises(mock_smtp_class, mock_env):
    """Ensure send_email retries on failures and eventually raises the exception."""
    mock_smtp_class.side_effect = Exception("Connection Refused")

    with pytest.raises(Exception, match="Connection Refused"):
        send_email("to@myfinancedomain.org", "Subject Line", "Body content.")

    # Should have called SMTP constructor 2 times (SMTP_RETRIES = 2 in mock_env)
    assert mock_smtp_class.call_count == 2


@patch("services.emailer.send_email")
def test_send_login_logout_emails(mock_send_email):
    """Verify high-level trigger methods successfully formats and forwards request to send_email."""
    send_login_email("user@example.com", "user@example.com")
    mock_send_email.assert_called_once()
    assert mock_send_email.call_args[0][0] == "user@example.com"
    assert "Login notification" in mock_send_email.call_args[0][1]

    mock_send_email.reset_mock()
    send_logout_email("user@example.com", "user@example.com")
    mock_send_email.assert_called_once()
    assert mock_send_email.call_args[0][0] == "user@example.com"
    assert "Logout notification" in mock_send_email.call_args[0][1]


@patch("services.emailer.send_email")
def test_send_password_reset_code_emails(mock_send_email):
    """Verify reset links and reset codes format parameters correctly."""
    send_password_reset_email("user@example.com", "http://reset-link", ttl_minutes=15)
    mock_send_email.assert_called_once()
    assert mock_send_email.call_args[0][0] == "user@example.com"
    assert "http://reset-link" in mock_send_email.call_args[0][2]
    assert "15 minutes" in mock_send_email.call_args[0][2]

    mock_send_email.reset_mock()
    send_reset_code_email("user@example.com", "888888", ttl_minutes=25)
    mock_send_email.assert_called_once()
    assert mock_send_email.call_args[0][0] == "user@example.com"
    assert "888888" in mock_send_email.call_args[0][2]
    assert "25 minutes" in mock_send_email.call_args[0][2]
