from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .models import CustomUser
from .forms import UserRegisterForm, ProfileCreateForm
from ..base.services import sent_email_register


class RegistrationUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'authorization/registration/register.html'
    success_url = reverse_lazy('register_to_email')

    def form_valid(self, form):
        sent_email_register(form.instance.email,
                            form.instance.username,
                            self.request)
        return super().form_valid(form)


class ToRegistrationUserEmail(TemplateView):
    template_name = 'authorization/registration/register_done.html'


class ProfileEdit(SuccessMessageMixin, UpdateView):
    form_class = ProfileCreateForm
    template_name = 'authorization/profile/profile_create.html'
    success_url = reverse_lazy('login')
    success_message = 'Data saved'

    def get_object(self, queryset=None):
        username = urlsafe_base64_decode(self.kwargs['uidb64'])
        return CustomUser.objects.get(username=bytes.decode(username, 'utf-8'))

    def form_valid(self, form):
        if not form.instance.activ_email:
            form.instance.activ_email = True
        return super().form_valid(form)
