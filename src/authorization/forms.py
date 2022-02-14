from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from src.authorization.models import CustomUser
from src.base.services import sent_email_register
from src.base import constants


class LoginForm(AuthenticationForm):

    def __init__(self, request, *args, **kwargs):
        super(LoginForm, self).__init__(request=None, *args, **kwargs)
        self._request = request
        self.fields['username'].label = 'Username or Email'

    def clean(self):
        username = self.cleaned_data.get('username')
        user = CustomUser.objects.filter(username=username).first() or CustomUser.objects.get(email=username).first()
        if user:
            if not user.activ_email:
                sent_email_register(email=user.email,
                                    username=user.username,
                                    request=self._request)
                raise ValidationError(constants.RAIS_LOGINFORM)
        super(LoginForm, self).clean()


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class ProfileCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileCreateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'required': True})
        self.fields['last_name'].widget.attrs.update({'required': True})

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'bio', 'avatar', 'activ_email',)
        widgets = {'activ_email': forms.HiddenInput()}
