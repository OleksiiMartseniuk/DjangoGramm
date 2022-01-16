from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic import TemplateView

from .models import CustomUser
from .forms import UserRegisterForm, ProfileForm


@login_required()
def index(request):
    user1 = CustomUser.objects.get(id=1)
    user2 = CustomUser.objects.get(id=2)
    user1.following.add(user2)

    return render(request, 'base.html')


class RegistrationUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'account/registration/register.html'
    success_url = reverse_lazy('register_to_email')


class ToRegistrationUserEmail(TemplateView):
    template_name = 'account/registration/register_done.html'




