from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_order_confirmation_email(order_id, user_email, user_name):
    subject = f"Your Order #{order_id} has been placed successfully!"
    message = f"Dear {user_name},\n\nThank you for your order. Your order #{order_id} has been successfully placed. We will notify you when your order is being processed."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    
    send_mail(subject, message, from_email, recipient_list)