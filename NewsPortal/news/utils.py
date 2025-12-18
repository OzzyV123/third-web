from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import CategorySub


def notify_subscribers(post):
    category = post.category

    subs = CategorySub.objects.filter(category=category).select_related('user')

    emails = [
        sub.user.email
        for sub in subs
        if sub.user.email
    ]

    if not emails:
        return

    subject = f'Новая публикация в категории "{category.name}"'
    message = (
        f'В категории "{category.name}" вышел новый материал:\n\n'
        f'{post.name}\n\n'
        f'{post.preview()}\n\n'
        f'Ссылка: http://127.0.0.1:8000{post.get_absolute_url()}'
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=None,  # возьмётся DEFAULT_FROM_EMAIL
        recipient_list=emails,
        fail_silently=False,
    )
