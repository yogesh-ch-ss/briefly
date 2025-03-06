from django.conf import settings
from django.core.mail import send_mail

def send_to_admin(message, user_email):
    subject = "New message from a user"
    message = "Message content\n" + message + "\n"
    message += "User email: " + user_email
    send_mail(
        subject, 
        message, 
        from_email=settings.EMAIL_HOST_USER, 
        recipient_list=[settings.EMAIL_HOST_USER]
    )

def send_to_user(message, user_email):
    subject = "[Briefly.] Your message has been received"
    message = "Message content\n" + message + "\n"
    message += "We will get back to you as soon as possible."
    message += "\n\n Briefly. Team"
    send_mail(
        subject, 
        message, 
        from_email=settings.EMAIL_HOST_USER, 
        recipient_list=[user_email]
    )