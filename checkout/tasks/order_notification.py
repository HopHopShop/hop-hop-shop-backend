from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task
def send_notification_mail(user_email: str) -> None:
    subject = "Order confirmation"
    from_email = "no-replay@hop-hop-shop.me"
    html_message = render_to_string("order_confirmation.html")

    send_mail(subject, html_message, from_email, [user_email])
