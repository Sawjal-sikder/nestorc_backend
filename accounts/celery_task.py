from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

@shared_task
def Celery_send_mail(email, message, subject):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False  # will raise errors if something goes wrong
    )
