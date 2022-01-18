from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from src.account.models import CustomUser
from src.base.services import get_or_none, sent_email_register


class LoginForm(AuthenticationForm):

    def __init__(self, request, *args, **kwargs):
        super(LoginForm, self).__init__(request=None, *args, **kwargs)
        self._request = request
        self.fields['username'].label = 'Username or Email'

    def clean(self):
        username = self.cleaned_data.get('username')
        user = get_or_none(CustomUser, username=username)
        if user:
            if not user.activ_email:
                sent_email_register(email=user.email,
                                    username=user.username,
                                    request=self._request)
                raise ValidationError('An email has been resent to you. Follow the link to complete registration')
        super(LoginForm, self).clean()


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'bio', 'avatar', 'activ_email',)
        widgets = {'activ_email': forms.HiddenInput()}
