from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def get_path_upload_avatar(instance, file):
    """Построения пути к файлу(avatar), format: (media)/avatar/user_id/photo.jpg"""
    return f'avatar/{instance.id}/{file}'


def sent_email_register(email: str, username: str, request: object):
    current_site = get_current_site(request)
    massege = render_to_string('account/registration/register_email.html', {
        'username': username,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(username)),
    })
    send_mail(subject='Registration email',
              message='One',
              html_message=massege,
              from_email='DjangoGram@email.com',
              recipient_list=[email])


