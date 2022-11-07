"""
Этот файл нужен для создания задач (D7).
Задачи это функции, которые можно использовать специальным обращением
и добавляя определенные параметры.
"""
from django.core.mail import EmailMultiAlternatives
from celery import shared_task
from django.template.loader import render_to_string
from datetime import *
from News_Portal import settings
from News_Portal.settings import SITE_URL

from news.models import Post, Category

@shared_task
def notify_about_new_post(instance):
        categories = instance.category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notification(instance.preview(), instance.pk, instance.post_title, subscribers)



@shared_task
def week_news_notification():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(post_date__gte=last_week)
    categories = set(posts.values_list('category__category_name', flat=True))
    subscribers = set(Category.objects.filter(category_name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_notification(preview, pk, post_title, subscribers):
    post = Post.objects.get(pk=pk)
    html_context = render_to_string(
        'post_created_email.html',
        {
            'text': post.post_text,
            'link': f'{SITE_URL}/news/{pk}',
            'post': post,
        }
    )

    msg = EmailMultiAlternatives(
        subject=post_title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()