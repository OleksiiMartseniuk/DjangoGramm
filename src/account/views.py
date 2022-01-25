import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin

from src.account.forms import CommentForm, PostCreateForm, EditProfileForm
from src.account.models import Post, Comment
from src.authorization.models import CustomUser
from django.http import JsonResponse
from django.http import HttpResponseRedirect

from src.base.services import like, subscription, delete_followers


@login_required()
def index(request):
    # user = CustomUser.objects.get(id=1)
    # user2 = CustomUser.objects.get(id=2)
    # user3 = CustomUser.objects.get(id=3)
    # user.following.add(user3)
    # user2.following.add(user)
    return render(request, 'base.html')


class ProfileListView(LoginRequiredMixin, ListView):
    """Profile user"""
    paginate_by = 6
    template_name = 'account/profile/profile_list.html'

    def get_queryset(self):
        return self.request.user.posts.filter(status='published').all()

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['section'] = 'profile'
        return super(ProfileListView, self).get_context_data(**kwargs)


class EditProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Edit profile user"""
    form_class = EditProfileForm
    template_name = 'account/profile/profile_edit.html'
    success_message = 'Profile updated'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.request.user.username})


class SubscriptionHandler(LoginRequiredMixin, View):
    """Handler button subscription"""
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        return JsonResponse(subscription(data, request, CustomUser))


class FollowersHandler(LoginRequiredMixin, View):
    """Handler button followers"""
    def get(self, request, *args, **kwargs):
        delete_followers(request, kwargs['user_id'], CustomUser)
        return HttpResponseRedirect(reverse('profile', kwargs={'username': self.request.user.username}))


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Create Post"""
    form_class = PostCreateForm
    template_name = 'account/image/image_create.html'
    success_url = reverse_lazy('home')
    success_message = 'Image add'

    def get_initial(self):
        initial = super().get_initial()
        initial['owner'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        kwargs['section'] = 'create'
        return super(PostCreateView, self).get_context_data(**kwargs)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """Delete Post"""
    template_name = 'account/image/image_delete.html'
    success_message = 'Images deleted successfully'

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse('profile', kwargs={'username': self.request.user.username})

    def get_queryset(self):
        return self.request.user.posts.all()


class ImageDetailView(LoginRequiredMixin, DetailView, FormMixin):
    """Image detail"""
    model = Post
    template_name = 'account/image/image_detail.html'
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


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    """Delete Comment"""
    template_name = 'account/comment/comment_delete.html'
    success_message = 'Comment deleted successfully'

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse('detail_image', kwargs={'slug': self.get_object().post.title})

    def get_queryset(self):
        return self.request.user.comments.all()


class LikeImageHandler(LoginRequiredMixin, View):
    """Handler button like"""
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        return JsonResponse(like(data, request, Post))
