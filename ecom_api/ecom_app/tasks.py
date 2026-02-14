from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_order_confirmation_email(order_id, user_email):
    subject = "order confirmation"
    message = f"your order for {order_id} has been received and being processed"

    return send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, {user_email})
