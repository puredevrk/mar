from flask_mail import Message
from app import mail

def send_notification(email, subject, body):
    msg = Message(subject, recipients=[email])
    msg.body = body
    mail.send(msg)
