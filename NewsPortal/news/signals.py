from django.db.models.signals import post_save
from .models import Post
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .tasks import send_new_post_email


@receiver(post_save, sender=Post)
def post_created(sender, instance, created, **kwargs):
    if created:
        send_new_post_email.delay(instance.id)


@receiver(user_signed_up)
def send_welcome_email(request, user, **kwargs):
    subject = 'Добро пожаловать на наш сайт!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    html_content = render_to_string('emails/welcome_email.html', {'user': user})

    email = EmailMultiAlternatives(subject=subject, body='', from_email=from_email, to=recipient_list)
    email.attach_alternative(html_content, "text/html")
    email.send()