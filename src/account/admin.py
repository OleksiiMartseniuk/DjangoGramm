from django.contrib import admin

from src.account.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'status')
    list_filter = ('create', 'owner')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'post', 'active')
    list_filter = ('owner', 'post', 'active')
