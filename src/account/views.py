from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .models import CustomUser
from .forms import UserRegisterForm, ProfileCreateForm
from ..base.services import sent_email_register


@login_required()
def index(request):
    user1 = CustomUser.objects.get(id=1)
    return render(request, 'base.html')


class RegistrationUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'account/registration/register.html'
    success_url = reverse_lazy('register_to_email')

    def form_valid(self, form):
        sent_email_register(form.instance.email,
                            form.instance.username,
                            self.request)
        return super().form_valid(form)


class ToRegistrationUserEmail(TemplateView):
    template_name = 'account/registration/register_done.html'


class ProfileEdit(UpdateView, SuccessMessageMixin):
    form_class = ProfileCreateForm
    template_name = 'account/profile/profile_create.html'
    success_url = reverse_lazy('login')
    success_message = 'Data saved'

    def get_object(self, queryset=None):
        username = urlsafe_base64_decode(self.kwargs['uidb64'])
        return CustomUser.objects.get(username=bytes.decode(username, 'utf-8'))

    def form_valid(self, form):
        if not form.instance.activ_email:
            form.instance.activ_email = True
        return super().form_valid(form)
