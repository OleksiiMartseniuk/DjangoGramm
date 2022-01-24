from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models import Model
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def get_path_upload_avatar(instance, file):
    """Построения пути к файлу(avatar), format: (media)/avatar/user_id/photo.jpg"""
    return f'avatar/{instance.id}/{file}'


def get_path_upload_image(instance, file):
    """Построения пути к файлу(image), format: (media)/image/user_id/photo.jpg"""
    return f'image/{instance.owner.id}/{file}'


def sent_email_register(email: str, username: str, request: object):
    current_site = get_current_site(request)
    massege = render_to_string('authorization/registration/register_email.html', {
        'username': username,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(username)),
    })
    send_mail(subject='Registration email',
              message='One',
              html_message=massege,
              from_email='DjangoGram@email.com',
              recipient_list=[email])


def get_or_none(class_model: Model, **kwargs: dict):
    try:
        return class_model.objects.get(**kwargs)
    except class_model.DoesNotExist:
        return None


def like(data: dict, request: object, model_post: Model) -> dict:
    post = get_or_none(model_post, id=data['id'])
    if post is None:
        return {'status': 'error'}
    if data['action'] == 'like':
        post.like.add(request.user)
        return {'status': 'ok'}
    elif data['action'] == 'unlike':
        post.like.remove(request.user)
        return {'status': 'ok'}


def subscription(data: dict, request: object, model_user: Model) -> dict:
    user_from = request.user
    user_to = model_user.objects.get(id=data['id'])
    if data['status']:
        user_from.following.add(user_to)
        return {'status': 'ok'}
    elif not data['status']:
        user_from.following.remove(user_to)
        return {'status': 'ok'}
    return {'status': 'error'}


def delete_followers(request: object, user_id: int, model_user: Model):
    user_from = request.user
    user_to = get_or_none(model_user, id=user_id)
    if user_to:
        user_to.following.remove(user_from)
