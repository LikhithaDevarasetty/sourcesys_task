from __future__ import annotations

import smtplib
from email.message import EmailMessage
import socket
from datetime import datetime, timezone
import time

from services.config import get_config
from services.logger import get_logger

logger = get_logger("finance_app.email")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _extract_username(email: str) -> str:
    """Extracts a friendly name from the email address's local part."""
    try:
        local_part = email.split("@")[0]
        # Replace common separators with spaces
        name_parts = local_part.replace(".", " ").replace("_", " ").replace("-", " ").split()
        # Capitalize each word and join them
        friendly_name = " ".join([p.capitalize() for p in name_parts])
        if friendly_name:
            return friendly_name
    except Exception:
        pass
    return "User"


def _build_html_template(heading: str, name: str, message_html: str) -> str:
    """Wraps message content inside a highly polished, responsive dark-glassmorphism HTML card.
    
    Using professional headers, clear fonts, and premium buttons significantly improves
    deliverability and prevents receiving email servers from flagging transactional emails as spam.
    """
    current_year = datetime.now(timezone.utc).year
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{heading}</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: #07090e;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            color: #f8fafc;
            -webkit-font-smoothing: antialiased;
        }}
        .wrapper {{
            width: 100%;
            table-layout: fixed;
            background-color: #07090e;
            padding: 40px 0;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #0d121e;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }}
        .header {{
            background: linear-gradient(135deg, #6366f1, #3b82f6);
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            color: #ffffff;
            font-size: 24px;
            font-weight: 800;
            letter-spacing: -0.03em;
        }}
        .content {{
            padding: 40px 30px;
            line-height: 1.6;
        }}
        .content p {{
            margin: 0 0 20px 0;
            font-size: 16px;
            color: #cbd5e1;
        }}
        .content h2 {{
            margin: 0 0 20px 0;
            color: #ffffff;
            font-size: 20px;
            font-weight: 700;
        }}
        .btn-container {{
            margin: 30px 0;
            text-align: center;
        }}
        .btn {{
            display: inline-block;
            background: linear-gradient(135deg, #6366f1, #3b82f6);
            color: #ffffff !important;
            text-decoration: none;
            padding: 12px 30px;
            font-weight: 700;
            border-radius: 12px;
            box-shadow: rgba(99, 102, 241, 0.25) 0px 4px 16px;
            font-size: 16px;
        }}
        .footer {{
            padding: 30px;
            background-color: rgba(0, 0, 0, 0.2);
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            text-align: center;
            font-size: 12px;
            color: #64748b;
        }}
        .bullet-list {{
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
            list-style-type: none;
        }}
        .bullet-list li {{
            margin-bottom: 12px;
            font-size: 15px;
            color: #cbd5e1;
            font-family: monospace, monospace;
        }}
        .bullet-list li:last-child {{
            margin-bottom: 0;
        }}
        .bullet-list strong {{
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="container">
            <div class="header">
                <h1>💸 RupeeTracker</h1>
            </div>
            <div class="content">
                <h2>Hi {name},</h2>
                {message_html}
            </div>
            <div class="footer">
                This is an automated security notification from your RupeeTracker account.<br>
                &copy; {current_year} RupeeTracker. All rights reserved.
            </div>
        </div>
    </div>
</body>
</html>
"""


def send_email(to_email: str, subject: str, plain_body: str, html_body: str | None = None) -> None:
    host = get_config("smtp", "host")
    port = int(get_config("smtp", "port", default="587"))
    username = get_config("smtp", "username")
    password = get_config("smtp", "password")
    sender = get_config("smtp", "from_email") or (username or "")

    def _looks_like_placeholder(val: str | None) -> bool:
        if not val:
            return True
        v = str(val).strip().lower()
        if v in ("", "change_me", "change-me", "change", "your-smtp-host", "your_smtp_host"):
            return True
        if "example" in v or "your" in v:
            return True
        return False

    if _looks_like_placeholder(host) or _looks_like_placeholder(username) or _looks_like_placeholder(sender) or not password:
        logger.warning("SMTP config appears to be a placeholder or incomplete; skipping email. to=%s subject=%s host=%r sender=%r username_set=%s",
                       to_email, subject, host, sender, bool(username))
        logger.info("Email plain body:\n%s", plain_body)
        return

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(plain_body)
    
    if html_body:
        msg.add_alternative(html_body, subtype="html")

    attempts = int(get_config("smtp", "retries", default="5"))
    backoff_base = float(get_config("smtp", "backoff_base", default="2"))
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
            logger.warning("SMTP send attempt %d/%d failed", attempt, attempts, exc_info=True)
            if attempt < attempts:
                sleep_secs = backoff_base * (2 ** (attempt - 1))
                time.sleep(sleep_secs)
    logger.exception("All SMTP send attempts failed for to=%s subject=%s", to_email, subject)
    raise last_exc


def send_login_email(to_email: str, email: str) -> None:
    friendly_name = _extract_username(email)
    subject = "Login notification — RupeeTracker"
    plain_body = (
        f"Hi there {friendly_name},\n\n"
        f"We detected a login to your RupeeTracker account.\n"
        f"Time (UTC): {_now_iso()}\n\n"
        f"If this wasn't you, please reset your password immediately.\n\n"
        f"— RupeeTracker Team"
    )
    message_html = (
        f"<p>We detected a new login to your RupeeTracker personal finance account.</p>"
        f"<ul class='bullet-list'>"
        f"<li><strong>Activity:</strong> Account Login</li>"
        f"<li><strong>Time (UTC):</strong> {_now_iso()}</li>"
        f"</ul>"
        f"<p>If this was you, you can safely ignore this message. If you do not recognize this activity, please change your password immediately to secure your account.</p>"
    )
    html_body = _build_html_template("Login Notification", friendly_name, message_html)
    send_email(to_email, subject, plain_body, html_body)


def send_logout_email(to_email: str, email: str) -> None:
    friendly_name = _extract_username(email)
    subject = "Logout notification — RupeeTracker"
    plain_body = (
        f"Hi there {friendly_name},\n\n"
        f"You have been successfully logged out of your RupeeTracker account.\n"
        f"Time (UTC): {_now_iso()}\n\n"
        f"— RupeeTracker Team"
    )
    message_html = (
        f"<p>You have been successfully logged out of your RupeeTracker account.</p>"
        f"<ul class='bullet-list'>"
        f"<li><strong>Activity:</strong> Account Logout</li>"
        f"<li><strong>Time (UTC):</strong> {_now_iso()}</li>"
        f"</ul>"
        f"<p>Thank you for using RupeeTracker to manage your finances securely!</p>"
    )
    html_body = _build_html_template("Logout Notification", friendly_name, message_html)
    send_email(to_email, subject, plain_body, html_body)


def send_password_reset_email(to_email: str, reset_link: str, recipient_name: str | None = None, ttl_minutes: int = 20) -> None:
    friendly_name = recipient_name or _extract_username(to_email)
    subject = "Reset your RupeeTracker password"
    plain_body = (
        f"Hi there {friendly_name},\n\n"
        f"We received a request to reset the password for your RupeeTracker account.\n\n"
        f"Use the link below to choose a new password (the link expires in {ttl_minutes} minutes):\n\n"
        f"{reset_link}\n\n"
        f"If you did not request a password reset, you can safely ignore this message.\n\n"
        f"— RupeeTracker Team"
    )
    message_html = (
        f"<p>We received a request to reset the password for your RupeeTracker account.</p>"
        f"<p>Click the button below to choose a new secure password. This request will expire in <strong>{ttl_minutes} minutes</strong>:</p>"
        f"<div class='btn-container'><a href='{reset_link}' class='btn'>Reset Password</a></div>"
        f"<p style='font-size: 13px; color: #64748b;'>If the button doesn't work, copy and paste this link into your browser:<br>"
        f"<a href='{reset_link}' style='color: #6366f1; word-break: break-all;'>{reset_link}</a></p>"
        f"<p>If you did not request a password reset, please ignore this email; your credentials will remain fully secure.</p>"
    )
    html_body = _build_html_template("Reset Password", friendly_name, message_html)
    send_email(to_email, subject, plain_body, html_body)


def send_reset_code_email(to_email: str, code: str, recipient_name: str | None = None, ttl_minutes: int = 20) -> None:
    friendly_name = recipient_name or _extract_username(to_email)
    subject = "Your RupeeTracker password reset code"
    plain_body = (
        f"Hi there {friendly_name},\n\n"
        f"Use the following one-time code to reset your RupeeTracker password:\n\n"
        f"Code: {code}\n\n"
        f"This code will expire in {ttl_minutes} minutes.\n\n"
        f"If you did not request this, you can safely ignore this message.\n\n"
        f"— RupeeTracker Team"
    )
    message_html = (
        f"<p>We received a request to reset your RupeeTracker password. Use the secure one-time code below to complete your reset:</p>"
        f"<div style='text-align: center; margin: 35px 0;'>"
        f"<span style='background: rgba(99, 102, 241, 0.1); border: 2px dashed #6366f1; color: #ffffff; font-size: 32px; font-weight: 800; padding: 12px 30px; border-radius: 12px; letter-spacing: 0.15em; display: inline-block;'>{code}</span>"
        f"</div>"
        f"<p>This code will expire in <strong>{ttl_minutes} minutes</strong>.</p>"
        f"<p>If you did not request this, you can safely ignore this message; your credentials will remain unchanged.</p>"
    )
    html_body = _build_html_template("Password Reset Code", friendly_name, message_html)
    send_email(to_email, subject, plain_body, html_body)


def send_budget_warning_email(to_email: str, budget_label: str, spent: float, limit: float, ratio_pct: int) -> None:
    friendly_name = _extract_username(to_email)
    subject = f"⚠️ Budget Warning — {budget_label} is at {ratio_pct}%"
    plain_body = (
        f"Hi there {friendly_name},\n\n"
        f"Your spending for \"{budget_label}\" is approaching the budget limit.\n\n"
        f"  • Budget Limit : ₹{limit:,.2f}\n"
        f"  • Amount Spent : ₹{spent:,.2f}\n"
        f"  • Usage        : {ratio_pct}%\n\n"
        f"You are nearing your budget cap. Consider reducing your spending in this category to stay within limits.\n\n"
        f"— RupeeTracker Budget Monitor"
    )
    message_html = (
        f"<p>Your spending for the category <strong>\"{budget_label}\"</strong> is approaching your configured limit.</p>"
        f"<ul class='bullet-list' style='border-left: 4px solid #f59e0b;'>"
        f"<li><strong>Category:</strong> {budget_label}</li>"
        f"<li><strong>Budget Limit:</strong> ₹{limit:,.2f}</li>"
        f"<li><strong>Amount Spent:</strong> ₹{spent:,.2f}</li>"
        f"<li><strong>Usage:</strong> <span style='color: #f59e0b; font-weight: 700;'>{ratio_pct}%</span></li>"
        f"</ul>"
        f"<p>You are approaching your budget cap. Consider adjusting your category spending to stay within your visual budget targets.</p>"
    )
    html_body = _build_html_template("Budget Warning Alert", friendly_name, message_html)
    send_email(to_email, subject, plain_body, html_body)


def send_budget_breach_email(to_email: str, budget_label: str, spent: float, limit: float, over_amount: float) -> None:
    friendly_name = _extract_username(to_email)
    subject = f"🚨 Budget Exceeded — {budget_label} is over by ₹{over_amount:,.2f}"
    plain_body = (
        f"Hi there {friendly_name},\n\n"
        f"CRITICAL: Your spending for \"{budget_label}\" has exceeded the budget limit!\n\n"
        f"  • Budget Limit  : ₹{limit:,.2f}\n"
        f"  • Amount Spent  : ₹{spent:,.2f}\n"
        f"  • Over by       : ₹{over_amount:,.2f}\n\n"
        f"Please review your recent transactions and take corrective action.\n\n"
        f"— RupeeTracker Budget Monitor"
    )
    message_html = (
        f"<p style='color: #ef4444; font-weight: 700;'>CRITICAL: Your spending for the category \"{budget_label}\" has breached your budget target!</p>"
        f"<ul class='bullet-list' style='border-left: 4px solid #ef4444;'>"
        f"<li><strong>Category:</strong> {budget_label}</li>"
        f"<li><strong>Budget Limit:</strong> ₹{limit:,.2f}</li>"
        f"<li><strong>Amount Spent:</strong> ₹{spent:,.2f}</li>"
        f"<li><strong>Overspending Amount:</strong> <span style='color: #ef4444; font-weight: 700;'>₹{over_amount:,.2f}</span></li>"
        f"</ul>"
        f"<p>We recommend reviewing your recent entries in the dashboard and adjusting your expenses to maintain healthy financial balance.</p>"
    )
    html_body = _build_html_template("Budget Limit Breached", friendly_name, message_html)
    send_email(to_email, subject, plain_body, html_body)


def send_expense_notification_email(
    to_email: str,
    recipient_name: str,
    tx_id: int,
    date_str: str,
    category: str,
    amount: float,
    notes: str | None,
    budget_alert: dict | None = None
) -> None:
    """Sends an transactional receipt email for a logged expense, incorporating live color-coded budget status updates."""
    friendly_name = recipient_name
    subject = f"💸 Expense Logged: ₹{amount:,.2f} under {category}"
    
    plain_body = (
        f"Hi {friendly_name},\n\n"
        f"A new expense entry has been logged to your RupeeTracker passbook:\n\n"
        f"  • Transaction ID : #{tx_id}\n"
        f"  • Date           : {date_str}\n"
        f"  • Category       : {category}\n"
        f"  • Amount         : ₹{amount:,.2f}\n"
        f"  • Remarks        : {notes or '—'}\n\n"
    )
    
    alert_box_html = ""
    if budget_alert:
        status = budget_alert["status"]
        limit = budget_alert["limit"]
        spent = budget_alert["spent"]
        ratio_pct = budget_alert["ratio_pct"]
        label = budget_alert["label"]
        
        plain_body += (
            f"--- BUDGET STATUS ALERT ({status.upper()}) ---\n"
            f"  • Target Budget  : {label}\n"
            f"  • Budget Limit   : ₹{limit:,.2f}\n"
            f"  • Amount Spent   : ₹{spent:,.2f}\n"
            f"  • Usage Ratio    : {ratio_pct}%\n\n"
        )
        
        if status == "red":
            over_amount = spent - limit
            alert_box_html = f"""
            <div style="background: rgba(239, 68, 68, 0.1) !important; border: 1px solid rgba(239, 68, 68, 0.25) !important; border-left: 5px solid #ef4444 !important; padding: 18px !important; border-radius: 12px !important; margin: 25px 0 !important;">
                <h3 style="color: #fca5a5 !important; margin: 0 0 8px 0 !important; font-size: 16px !important; font-weight: 700 !important; font-family: -apple-system, sans-serif !important;">🚨 Critical: Budget Limit Exceeded!</h3>
                <p style="color: #fecaca !important; margin: 0 !important; font-size: 14px !important; line-height: 1.5 !important;">
                    Your spending for <strong>"{label}"</strong> has breached your budget cap! You are over budget by <strong>₹{over_amount:,.2f}</strong>.
                </p>
                <div style="color: #f87171 !important; margin-top: 12px !important; font-size: 13px !important; font-weight: 600 !important; font-family: monospace !important;">
                    Limit: ₹{limit:,.2f} | Spent: ₹{spent:,.2f} ({ratio_pct}%)
                </div>
            </div>
            """
        elif status == "orange":
            alert_box_html = f"""
            <div style="background: rgba(245, 158, 11, 0.1) !important; border: 1px solid rgba(245, 158, 11, 0.25) !important; border-left: 5px solid #f59e0b !important; padding: 18px !important; border-radius: 12px !important; margin: 25px 0 !important;">
                <h3 style="color: #fde047 !important; margin: 0 0 8px 0 !important; font-size: 16px !important; font-weight: 700 !important; font-family: -apple-system, sans-serif !important;">⚠️ Warning: Budget Limit Nearing!</h3>
                <p style="color: #fef08a !important; margin: 0 !important; font-size: 14px !important; line-height: 1.5 !important;">
                    Your spending for <strong>"{label}"</strong> is approaching your budget limit. You have consumed <strong>{ratio_pct}%</strong> of your allowed cap.
                </p>
                <div style="color: #fbbf24 !important; margin-top: 12px !important; font-size: 13px !important; font-weight: 600 !important; font-family: monospace !important;">
                    Limit: ₹{limit:,.2f} | Spent: ₹{spent:,.2f} ({ratio_pct}%)
                </div>
            </div>
            """
        elif status == "green":
            alert_box_html = f"""
            <div style="background: rgba(16, 185, 129, 0.1) !important; border: 1px solid rgba(16, 185, 129, 0.25) !important; border-left: 5px solid #10b981 !important; padding: 18px !important; border-radius: 12px !important; margin: 25px 0 !important;">
                <h3 style="color: #6ee7b7 !important; margin: 0 0 8px 0 !important; font-size: 16px !important; font-weight: 700 !important; font-family: -apple-system, sans-serif !important;">✅ Safe: Budget within Healthy Limits</h3>
                <p style="color: #a7f3d0 !important; margin: 0 !important; font-size: 14px !important; line-height: 1.5 !important;">
                    Your spending for <strong>"{label}"</strong> is well within your safe financial targets. You have used <strong>{ratio_pct}%</strong> of your budget.
                </p>
                <div style="color: #34d399 !important; margin-top: 12px !important; font-size: 13px !important; font-weight: 600 !important; font-family: monospace !important;">
                    Limit: ₹{limit:,.2f} | Spent: ₹{spent:,.2f} ({ratio_pct}%)
                </div>
            </div>
            """

    plain_body += "— RupeeTracker Team"
    
    message_html = f"""
    <p>A new expense entry has been successfully logged to your RupeeTracker passbook.</p>
    <ul class="bullet-list">
        <li><strong>Reference ID:</strong> #{tx_id}</li>
        <li><strong>Log Date:</strong> {date_str}</li>
        <li><strong>Category:</strong> {category}</li>
        <li><strong>Amount:</strong> ₹{amount:,.2f}</li>
        <li><strong>Notes/Remarks:</strong> {notes or '—'}</li>
    </ul>
    {alert_box_html}
    <p>You can view your complete passbook history and manage your monthly categories by opening your dashboard.</p>
    """
    
    html_body = _build_html_template("Expense Entry Notification", friendly_name, message_html)
    send_email(to_email, subject, plain_body, html_body)

