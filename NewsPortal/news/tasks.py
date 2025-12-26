from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from datetime import timedelta
from django.utils.timezone import now

from .models import Post, CategorySub

User = get_user_model()

@shared_task
def send_new_post_email(post_id):

    post = Post.objects.select_related('category').get(id=post_id)

    subs = CategorySub.objects.filter(
        category=post.category
    ).select_related('user')

    emails = [sub.user.email for sub in subs if sub.user.email]

    if not emails:
        return 'no subscribers'

    send_mail(
        subject=f'Новая публикация в категории "{post.category.name}"',
        message=f'''
    {post.name}

    {post.preview()}

    Ссылка:
    http://127.0.0.1:8000{post.get_absolute_url()}
    ''',
        from_email=None,
        recipient_list=emails,
    )

    return f'sent {len(emails)} emails'

@shared_task
def weekly_digest():
    from .models import Post, CategorySub

    week_ago = now() - timedelta(days=7)

    posts = Post.objects.filter(timestamp__gte=week_ago)

    if not posts.exists():
        return 'no posts'

    for sub in CategorySub.objects.select_related('user', 'category'):
        user_posts = posts.filter(category=sub.category)

        if not user_posts.exists():
            continue

        message = 'Новости за неделю:\n\n'
        for post in user_posts:
            message += f'- {post.name}\n'

        send_mail(
            subject='Еженедельная подборка новостей',
            message=message,
            from_email=None,
            recipient_list=[sub.user.email],
        )

    return 'weekly digest sent'