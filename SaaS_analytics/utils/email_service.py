# utils/email_service.py
import os
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

MOCK_EMAIL_LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sent_emails_log.txt")

def _send_email_worker(subject, recipient, html_body, smtp_config=None):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    is_real_smtp = False
    
    if smtp_config and smtp_config.get("host") and smtp_config.get("username") and smtp_config.get("password"):
        is_real_smtp = not smtp_config.get("demo_mode", False)
        
    if is_real_smtp:
        try:
            host = smtp_config["host"]
            port = int(smtp_config.get("port", 587))
            username = smtp_config["username"]
            password = smtp_config["password"]
            sender = smtp_config.get("sender_email", username) or "no-reply@saas-analytics.com"
            
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"SaaS Analytics <{sender}>"
            msg["To"] = recipient
            msg.attach(MIMEText(html_body, "html"))
            
            if port == 465:
                server = smtplib.SMTP_SSL(host, port, timeout=10)
                server.login(username, password)
            else:
                server = smtplib.SMTP(host, port, timeout=10)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(username, password)
                
            server.sendmail(sender, [recipient], msg.as_string())
            server.quit()
            
            with open(MOCK_EMAIL_LOG, "a", encoding="utf-8") as f:
                f.write(f"[{now_str}] SUCCESS: Email sent to <{recipient}>. Subject: {subject}\n")
            return
            
        except Exception as e:
            with open(MOCK_EMAIL_LOG, "a", encoding="utf-8") as f:
                f.write(f"[{now_str}] ERROR: SMTP send failure to <{recipient}>: {str(e)}. Fallback to demo.\n")
            is_real_smtp = False
            
    if not is_real_smtp:
        try:
            with open(MOCK_EMAIL_LOG, "a", encoding="utf-8") as f:
                f.write(f"\n" + "="*80 + f"\n")
                f.write(f"[{now_str}] EMAIL DISPATCH SIMULATION\n")
                from_addr = smtp_config.get("sender_email", "no-reply@saas-analytics.com") if smtp_config else "no-reply@saas-analytics.com"
                f.write(f"FROM: {from_addr}\n")
                f.write(f"TO: {recipient}\n")
                f.write(f"SUBJECT: {subject}\n")
                f.write(f"BODY:\n{html_body}\n")
                f.write("="*80 + "\n")
        except Exception as log_err:
            print(f"Error logging mock email: {log_err}")


def send_login_email_async(user_email, smtp_config=None, client_info=None):
    if not user_email:
        return
        
    client_info = client_info or {}
    ip = client_info.get("ip", "127.0.0.1")
    browser = client_info.get("browser", "Chrome / Windows 10")
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    subject = "Security Alert: New Sign-in detected"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f4f6f9; color: #333; margin: 0; padding: 30px 10px; }}
            .container {{ max-width: 550px; margin: 0 auto; background: #ffffff; border: 1px solid #e1e4e8; border-radius: 8px; padding: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
            .header {{ font-size: 18px; font-weight: bold; border-bottom: 1px solid #e1e4e8; padding-bottom: 15px; margin-bottom: 20px; color: #00cec9; }}
            .details-table {{ width: 100%; margin: 15px 0; border-collapse: collapse; }}
            .details-table td {{ padding: 8px 12px; border-bottom: 1px solid #f1f3f5; }}
            .label {{ color: #7f8c8d; font-weight: 500; width: 35%; }}
            .value {{ color: #2c3e50; font-weight: 600; }}
            .footer {{ margin-top: 25px; text-align: center; font-size: 11px; color: #95a5a6; border-top: 1px solid #e1e4e8; padding-top: 15px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">Security Alert: New Sign-In</div>
            <p>A new sign-in was detected on your SaaS Analytics account.</p>
            <table class="details-table">
                <tr><td class="label">Email</td><td class="value">{user_email}</td></tr>
                <tr><td class="label">Date</td><td class="value">{timestamp}</td></tr>
                <tr><td class="label">IP Address</td><td class="value">{ip}</td></tr>
                <tr><td class="label">Device</td><td class="value">{browser}</td></tr>
            </table>
            <p style="color: #e67e22; font-size: 13px;">If you do not recognize this activity, please reset your password immediately.</p>
            <div class="footer">SaaS Analytics Security Services</div>
        </div>
    </body>
    </html>
    """
    
    t = threading.Thread(target=_send_email_worker, args=(subject, user_email, html_body, smtp_config))
    t.daemon = True
    t.start()


def send_password_reset_email_async(user_email, smtp_config=None):
    if not user_email:
        return None
        
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    reset_token = "SAAS-RESET-" + os.urandom(8).hex().upper()
    subject = "Action Required: Reset your password"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f4f6f9; color: #333; margin: 0; padding: 30px 10px; }}
            .container {{ max-width: 550px; margin: 0 auto; background: #ffffff; border: 1px solid #e1e4e8; border-radius: 8px; padding: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
            .header {{ font-size: 18px; font-weight: bold; border-bottom: 1px solid #e1e4e8; padding-bottom: 15px; margin-bottom: 20px; color: #6c5ce7; }}
            .code {{ background: #f8f9fa; border: 1px dashed #6c5ce7; padding: 12px; border-radius: 6px; font-family: monospace; font-size: 18px; font-weight: bold; text-align: center; margin: 15px 0; color: #6c5ce7; }}
            .footer {{ margin-top: 25px; text-align: center; font-size: 11px; color: #95a5a6; border-top: 1px solid #e1e4e8; padding-top: 15px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">Password Reset Request</div>
            <p>We received a password reset request for your account on {timestamp}.</p>
            <p>Use the temporary verification code below to authorize your password update:</p>
            <div class="code">{reset_token}</div>
            <p style="font-size: 12px; color: #7f8c8d;">This security code is active for 24 hours. If you did not make this request, you can safely ignore this email.</p>
            <div class="footer">SaaS Analytics Security Services</div>
        </div>
    </body>
    </html>
    """
    
    t = threading.Thread(target=_send_email_worker, args=(subject, user_email, html_body, smtp_config))
    t.daemon = True
    t.start()
    return reset_token


def send_welcome_email_async(user_email, name, smtp_config=None):
    if not user_email:
        return
        
    subject = "Welcome to SaaS Analytics!"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f4f6f9; color: #333; margin: 0; padding: 30px 10px; }}
            .container {{ max-width: 550px; margin: 0 auto; background: #ffffff; border: 1px solid #e1e4e8; border-radius: 8px; padding: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
            .header {{ font-size: 18px; font-weight: bold; border-bottom: 1px solid #e1e4e8; padding-bottom: 15px; margin-bottom: 20px; color: #00cec9; }}
            .footer {{ margin-top: 25px; text-align: center; font-size: 11px; color: #95a5a6; border-top: 1px solid #e1e4e8; padding-top: 15px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">Welcome to SaaS Analytics!</div>
            <p>Hi {name},</p>
            <p>Your platform account has been successfully created. We are excited to help you analyze business metrics and predict churn!</p>
            <p>Your registered login identity is: <strong>{user_email}</strong></p>
            <p>Sign in anytime to access your dashboards and prediction panels.</p>
            <div class="footer">SaaS Analytics Team</div>
        </div>
    </body>
    </html>
    """
    
    t = threading.Thread(target=_send_email_worker, args=(subject, user_email, html_body, smtp_config))
    t.daemon = True
    t.start()


def send_logout_email_async(user_email, name=None, smtp_config=None):
    if not user_email:
        return
        
    name = name or user_email.split("@")[0].capitalize()
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    subject = "Security Notification: Successful Logout"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f4f6f9; color: #333; margin: 0; padding: 30px 10px; }}
            .container {{ max-width: 550px; margin: 0 auto; background: #ffffff; border: 1px solid #e1e4e8; border-radius: 8px; padding: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
            .header {{ font-size: 18px; font-weight: bold; border-bottom: 1px solid #e1e4e8; padding-bottom: 15px; margin-bottom: 20px; color: #fdcb6e; }}
            .footer {{ margin-top: 25px; text-align: center; font-size: 11px; color: #95a5a6; border-top: 1px solid #e1e4e8; padding-top: 15px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">Successful Session Logout</div>
            <p>Hi {name},</p>
            <p>Your session on SaaS Analytics has been successfully terminated on {timestamp}.</p>
            <p>This confirms that your active session token was securely cleared from this browser.</p>
            <div class="footer">SaaS Analytics Security Services</div>
        </div>
    </body>
    </html>
    """
    
    t = threading.Thread(target=_send_email_worker, args=(subject, user_email, html_body, smtp_config))
    t.daemon = True
    t.start()
