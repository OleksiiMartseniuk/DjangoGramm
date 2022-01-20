from django import forms

from src.account.models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('owner', 'post', 'text')
        widgets = {
            'owner': forms.HiddenInput(),
            'post': forms.HiddenInput(),
        }


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'image', 'description', 'owner')
        widgets = {
            'owner': forms.HiddenInput(),
        }
