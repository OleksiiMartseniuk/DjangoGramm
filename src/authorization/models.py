from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

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

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.username})
