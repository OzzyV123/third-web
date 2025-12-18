from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail

from .models import Post, Category, CategorySub


def send_weekly_digest():
    week_ago = timezone.now() - timedelta(days=7)

    for category in Category.objects.all():
        posts = Post.objects.filter(
            category=category,
            timestamp__gte=week_ago
        )

        if not posts.exists():
            continue

        subs = CategorySub.objects.filter(category=category).select_related('user')
        emails = [s.user.email for s in subs if s.user.email]

        if not emails:
            continue

        subject = f'Еженедельная подборка: {category.name}'
        lines = [
            f'За последнюю неделю в категории "{category.name}" появились новые материалы:\n'
        ]

        for post in posts:
            lines.append(
                f'- {post.name}\n'
                f'  http://127.0.0.1:8000{post.get_absolute_url()}'
            )

        send_mail(
            subject=subject,
            message='\n'.join(lines),
            from_email=None,
            recipient_list=emails,
            fail_silently=False,
        )