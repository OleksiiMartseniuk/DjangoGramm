from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from src.authorization.models import CustomUser


@login_required()
def index(request):
    # user = CustomUser.objects.get(id=1)
    # user2 = CustomUser.objects.get(id=2)
    # user.following.add(user2)
    return render(request, 'base.html')


class ProfileListView(LoginRequiredMixin, ListView):
    paginate_by = 6
    template_name = 'account/profile/profile.html'

    def get_queryset(self):
        return self.request.user.posts.filter(status='published').all()
