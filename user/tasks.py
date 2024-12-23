from django.template.loader import render_to_string
from django.utils import timezone
from user_agents import parse

from CalendarApp.celery import app

from celery import shared_task

from django.core.mail import send_mail
from django.conf import settings

from .models import PasswordResetSession


@app.task
def add(x, y):
    return x + y


@shared_task
def expire_password_reset_session(token):
    try:
        session = PasswordResetSession.objects.get(token=token)
        expiration_time = session.created_at.timestamp() + settings.PASSWORD_RESET_SESSION_TIMEOUT
        if timezone.now().timestamp() > expiration_time:
            session.delete()
    except PasswordResetSession.DoesNotExist:
        pass


@shared_task
def send_password_reset_email_task(
        email,
        reset_url,
        user_name,
        website_name,
        request_meta
):
    user_agent = parse(request_meta)

    context = {
        'action_url': reset_url,
        'name': user_name,
        'browser_name': user_agent.browser.family,
        'operating_system': user_agent.os.family,
        'website_name': settings.WEBSITE_NAME,
        'website_url': website_name
    }

    send_mail(
        subject='Password Reset Request',
        message=render_to_string(
            'authentication/partials/password_reset_email.txt',
            context=context
        ),
        html_message=render_to_string(
            'authentication/partials/reset-password-email.html',
            context=context
        ),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
