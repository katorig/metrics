import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dynaconf import settings


def send_email(send_from: str,
               send_to: str,
               subject: str,
               text: str) -> None:
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = send_from
    msg['To'] = send_to
    msg_text = MIMEText(text, 'plain')
    msg.attach(msg_text)
    s = smtplib.SMTP('webmail.tele2.ru')
    s.send_message(msg)
    s.quit()


def send_email_to_segmentation(model_id, report_date):
    send_email(settings.EMAIL_SEND_FROM,
               settings.SEGMENTATION.EMAIL_SEND_TO,
               settings.SEGMENTATION.SUBJECT.format(model_id, report_date),
               settings.SEGMENTATION.MESSAGE.format(model_id))
