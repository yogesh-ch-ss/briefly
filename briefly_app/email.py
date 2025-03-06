from django.conf import settings
from django.core.mail import send_mail

def send_to_admin(subject, message):
    send_mail(
        subject, 
        message, 
        from_email=settings.EMAIL_HOST_USER, 
        recipient_list=[settings.EMAIL_HOST_USER]
    )

def send_to_user(subject, message, user_email):
    send_mail(
        subject, 
        message, 
        from_email=settings.EMAIL_HOST_USER, 
        recipient_list=[user_email]
    )