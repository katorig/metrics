import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys


def send_email(send_to: str,
               subject: str,
               text: str) -> None:
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = 'metrics@info.tele2.ru'
    msg['To'] = send_to
    msg_text = MIMEText(text, 'plain')
    msg.attach(msg_text)
    s = smtplib.SMTP('webmail.tele2.ru')
    s.send_message(msg)
    s.quit()


def notification(*email_args):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if result == 'Error! Send notification':
                send_email(*email_args)
                sys.exit(1)
            return result
        return wrapper
    return decorator

