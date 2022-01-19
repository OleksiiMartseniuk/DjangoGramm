from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from django.conf import settings

from src.base.services import get_path_upload_image


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='posts',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    image = models.ImageField(upload_to=get_path_upload_image)
    description = models.TextField()
    like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                  related_name='likes',
                                  blank=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='published')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detail_image', kwargs={'slug': self.slug})


class Comment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='comments',
                              on_delete=models.CASCADE)
    post = models.ForeignKey(Post,
                             related_name='comments',
                             on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    create = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'comment: {self.post.title}, owner: {self.owner.username}'
