from django.contrib import admin

from src.account.models import Post, Comment

admin.site.register(Post)
admin.site.register(Comment)
