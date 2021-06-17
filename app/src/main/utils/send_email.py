import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
from dynaconf import settings


def send_email(kwargs) -> str:
    msg = MIMEMultipart()
    msg['To'] = kwargs['send_to']
    msg['Subject'] = kwargs['subject']
    msg['From'] = settings.SEND_EMAIL_FROM
    msg_text = MIMEText(kwargs['text'], 'plain')
    msg.attach(msg_text)
    s = smtplib.SMTP('webmail.tele2.ru')
    s.send_message(msg)
    s.quit()
    return 'Notification was sent'


def notification(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result == 'Error! Send notification':
            if kwargs.__contains__('send_to'):
                if kwargs['send_to'] is not None:
                    send_email(kwargs)
                    sys.exit(1)
                else:
                    sys.exit(1)
            else:
                sys.exit(1)
        return result
    return wrapper
