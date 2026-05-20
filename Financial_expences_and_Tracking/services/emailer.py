from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
import socket
from datetime import datetime, timezone
import time

from services.logger import get_logger

logger = get_logger("finance_app.email")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def send_email(to_email: str, subject: str, body: str) -> None:
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    # Accept either SMTP_USERNAME or legacy SMTP_USER
    username = os.getenv("SMTP_USERNAME") or os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    # Accept either EMAIL_FROM or legacy SMTP_FROM
    sender = os.getenv("EMAIL_FROM") or os.getenv("SMTP_FROM") or (username or "")

    # Detect placeholder/template values and skip sending (avoid noisy tracebacks)
    def _looks_like_placeholder(val: str | None) -> bool:
        if not val:
            return True
        v = val.strip().lower()
        if v in ("", "change_me", "change-me", "change", "your-smtp-host", "your_smtp_host"):
            return True
        if "example" in v or "your" in v:
            return True
        return False

    if _looks_like_placeholder(host) or _looks_like_placeholder(username) or _looks_like_placeholder(sender) or not password:
        logger.warning("SMTP config appears to be a placeholder or incomplete; skipping email. to=%s subject=%s host=%r sender=%r username_set=%s",
                       to_email, subject, host, sender, bool(username))
        logger.info("Email body:\n%s", body)
        return

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    # Attempt send with a retry/backoff for transient network/DNS failures
    attempts = int(os.getenv("SMTP_RETRIES", "5"))
    backoff_base = float(os.getenv("SMTP_BACKOFF_BASE", "2"))
    # Try to resolve the host to an IP and log it for debugging (non-fatal)
    try:
        resolved_ip = socket.gethostbyname(host)
        logger.info("Resolved SMTP host %s -> %s", host, resolved_ip)
    except Exception:
        logger.warning("Failed to resolve SMTP host %s", host, exc_info=True)
    last_exc = None
    for attempt in range(1, attempts + 1):
        try:
            with smtplib.SMTP(host, port, timeout=10) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(msg)
            return
        except Exception as e:
            last_exc = e
            # Include full traceback for debugging intermittent DNS/connectivity issues
            logger.warning("SMTP send attempt %d/%d failed", attempt, attempts, exc_info=True)
            if attempt < attempts:
                sleep_secs = backoff_base * (2 ** (attempt - 1))
                time.sleep(sleep_secs)
    # All attempts failed — log full exception and re-raise for callers to handle
    logger.exception("All SMTP send attempts failed for to=%s subject=%s", to_email, subject)
    raise last_exc


def send_login_email(to_email: str, email: str) -> None:
    subject = "Login notification — Finance Tracker"
    body = (
        f"Hi {email},\n\n"
        f"We detected a login to your Finance Tracker account.\n"
        f"Time (UTC): {_now_iso()}\n\n"
        f"If this wasn’t you, please reset your password immediately.\n\n"
        f"— Finance Tracker"
    )
    send_email(to_email, subject, body)


def send_logout_email(to_email: str, email: str) -> None:
    subject = "Logout notification — Finance Tracker"
    body = (
        f"Hi {email},\n\n"
        f"You have been logged out of your Finance Tracker account.\n"
        f"Time (UTC): {_now_iso()}\n\n"
        f"— Finance Tracker"
    )
    send_email(to_email, subject, body)


def send_password_reset_email(to_email: str, reset_link: str, recipient_name: str | None = None, ttl_minutes: int = 20) -> None:
    """Send a password reset email with a provided one-time reset link.

    This uses the generic `send_email` helper so behavior (retry/backoff/placeholders)
    is consistent with other notification emails.
    """
    name = recipient_name or to_email
    subject = "Reset your RupeeTracker password"
    body = (
        f"Hi {name},\n\n"
        "We received a request to reset the password for your RupeeTracker account.\n\n"
        f"Use the link below to choose a new password (the link expires in {ttl_minutes} minutes):\n\n{reset_link}\n\n"
        "If you did not request a password reset, you can safely ignore this message.\n\n"
        "— RupeeTracker Team"
    )
    send_email(to_email, subject, body)


def send_reset_code_email(to_email: str, code: str, recipient_name: str | None = None, ttl_minutes: int = 20) -> None:
    """Send a numeric/alphanumeric reset code to the user's email."""
    name = recipient_name or to_email
    subject = "Your RupeeTracker password reset code"
    body = (
        f"Hi {name},\n\n"
        "Use the following one-time code to reset your RupeeTracker password.\n\n"
        f"Code: {code}\n\n"
        f"This code will expire in {ttl_minutes} minutes.\n\n"
        "If you did not request this, you can safely ignore this message.\n\n"
        "— RupeeTracker Team"
    )
    send_email(to_email, subject, body)

