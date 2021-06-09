import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys


def send_email(kwargs) -> None:
    msg = MIMEMultipart()
    msg['Subject'] = kwargs['subject']
    msg['From'] = 'metrics@info.tele2.ru'
    msg['To'] = kwargs['send_to']
    msg_text = MIMEText(kwargs['text'], 'plain')
    msg.attach(msg_text)
    s = smtplib.SMTP('webmail.tele2.ru')
    s.send_message(msg)
    s.quit()


def notification(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if kwargs.__contains__('send_to'):
            if result == 'Error! Send notification':
                send_email(kwargs)
                sys.exit(1)
            return result
    return wrapper


@notification
def foo(x, **kwargs):
    print(kwargs)
    print(x + 1)
    return 'Error! Send notification'


if __name__ == '__main__':
    # {'send_to': 'ekaterina.gruzdova@tele2.ru', 'subject': 'TEST', 'text': 'test'}
    foo(10) #, send_to='ekaterina.gruzdova@tele2.ru', subject='TEST', text='test')


