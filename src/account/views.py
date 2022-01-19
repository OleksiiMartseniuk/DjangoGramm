from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from src.account.forms import CommentForm
from src.account.models import Post, Comment
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

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['section'] = 'profile'
        return super(ProfileListView, self).get_context_data(**kwargs)


class ImageDetailView(DetailView, FormMixin):
    model = Post
    template_name = 'account/profile/image_detail.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('detail_image', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        kwargs['comments_list'] = Comment.objects.filter(post=self.object, active=True).all()
        return super(ImageDetailView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial['owner'] = self.request.user
        initial['post'] = self.object
        return initial

    def form_valid(self, form):
        form.save()
        return super(ImageDetailView, self).form_valid(form)