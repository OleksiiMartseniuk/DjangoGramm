from django.db import models
from django.contrib.auth.models import AbstractUser

from src.actions.utils import create_action
from src.base import constants
from src.base.services import get_path_upload_avatar


class Contact(models.Model):
    user_from = models.ForeignKey('CustomUser',
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey('CustomUser',
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


class CustomUser(AbstractUser):
    email = models.EmailField()
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to=get_path_upload_avatar,
                               blank=True,
                               null=True)
    activ_email = models.BooleanField(default=False)
    following = models.ManyToManyField('self',
                                       through=Contact,
                                       related_name='followers',
                                       symmetrical=False)

    def subscription(self, data: dict, user_to: object) -> dict:
        """Handler subscription"""
        if data['status']:
            self.following.add(user_to)
            # add actions following
            create_action(self, constants.FOLLOWING, user_to)
            return {'status': 'ok'}
        elif not data['status']:
            self.following.remove(user_to)
            return {'status': 'ok'}
        return {'status': 'error'}

    def delete_followers(self, user: object):
        """Delete followers"""
        self.following.remove(user)
