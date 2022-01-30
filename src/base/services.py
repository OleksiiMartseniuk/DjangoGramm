from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Model, QuerySet
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.postgres.search import TrigramSimilarity

from src.actions.utils import create_action
from src.base import constants


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


def get_or_none(class_model: Model, **kwargs: dict):
    """Check objects exists"""
    try:
        return class_model.objects.get(**kwargs)
    except class_model.DoesNotExist:
        return None


def like(data: dict, request: object, model_post: Model) -> dict:
    """Handler like"""
    post = get_or_none(model_post, id=data['id'])
    if post is None:
        return {'status': 'error'}
    if data['action'] == 'like':
        post.like.add(request.user)
        # add actions like
        create_action(request.user, constants.LIKES, post)
        return {'status': 'ok'}
    elif data['action'] == 'unlike':
        post.like.remove(request.user)
        return {'status': 'ok'}


def subscription(data: dict, request: object, model_user: Model) -> dict:
    """Handler subscription"""
    user_from = request.user
    user_to = model_user.objects.get(id=data['id'])
    if data['status']:
        user_from.following.add(user_to)
        # add actions following
        create_action(user_from, constants.FOLLOWING, user_to)
        return {'status': 'ok'}
    elif not data['status']:
        user_from.following.remove(user_to)
        return {'status': 'ok'}
    return {'status': 'error'}


def delete_followers(request: object, user_id: int, model_user: Model):
    """Delete followers"""
    user_from = request.user
    user_to = get_or_none(model_user, id=user_id)
    if user_to:
        user_to.following.remove(user_from)


def get_search(query: str, model_user: Model) -> QuerySet:
    """QuerySet search"""
    return model_user.objects.annotate(
        similarity=TrigramSimilarity('first_name', query),
    ).filter(similarity__gt=0.3).order_by('-similarity')

