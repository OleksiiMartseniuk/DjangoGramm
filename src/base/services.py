from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Model, QuerySet
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.postgres.search import TrigramSimilarity


def get_path_upload_avatar(instance, file):
    """Path file(avatar), format: (media)/avatar/user_id/photo.jpg"""
    return f'avatar/{instance.id}/{file}'


def get_path_upload_image(instance, file):
    """Path file (image), format: (media)/image/user_id/photo.jpg"""
    return f'image/{instance.owner.id}/{file}'


def sent_email_register(email: str, username: str, request: object):
    """Sending email"""
    current_site = get_current_site(request)
    massege = render_to_string('authorization/registration/register_email.html', {
        'username': username,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(username)),
    })
    send_mail(subject='Registration email',
              message='One',
              html_message=massege,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[email])


def get_search(query: str, model_user: Model) -> QuerySet:
    """QuerySet search"""
    return model_user.objects.annotate(
        similarity=TrigramSimilarity('first_name', query),
    ).filter(similarity__gt=0.3).order_by('-similarity')

