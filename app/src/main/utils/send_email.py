import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
from dynaconf import settings as envs


def send_email(text='error, empty text') -> str:
    msg = MIMEMultipart()
    msg['To'] = envs.M_SEND_TO
    msg['Subject'] = f'Ошибка модели {envs.M_MODEL_ID}'
    msg['From'] = envs.SEND_EMAIL_FROM
    msg_text = MIMEText(text, 'plain')
    msg.attach(msg_text)
    s = smtplib.SMTP('webmail.tele2.ru')
    s.send_message(msg)
    s.quit()
    return 'Notification was sent'


def notification(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result[0] == 'Error! Stop':
            if result[1] == 1:
                send_email(result[2])
            sys.exit(1)
        return result
    return wrapper
