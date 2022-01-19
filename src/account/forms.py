from django import forms

from src.account.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('owner', 'post', 'text')
        widgets = {
            'owner': forms.HiddenInput(),
            'post': forms.HiddenInput(),
        }
