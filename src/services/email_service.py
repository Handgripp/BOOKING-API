import smtplib
from email.message import EmailMessage


mail_config = {
    'MAIL_SERVER': 'smtp.ethereal.email',
    'MAIL_PORT': 587,
    'MAIL_USE_TLS': True,
    'MAIL_DEFAULT_SENDER': 'lorenzo.kovacek52@ethereal.emai',
    'MAIL_USERNAME': 'lorenzo.kovacek52@ethereal.email',
    'MAIL_PASSWORD': 'bkBFaJGekNkfXGPQvz',
}


def send_mail(send_to, subject, body):
    msg = EmailMessage()
    msg["from"] = 'lorenzo.kovacek52@ethereal.email'
    msg["to"] = send_to
    msg["subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP(mail_config['MAIL_SERVER'], mail_config['MAIL_PORT']) as server:
        server.starttls()
        server.login(mail_config['MAIL_USERNAME'], mail_config['MAIL_PASSWORD'])
        server.send_message(msg)



