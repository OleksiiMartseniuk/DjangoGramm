from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from src.actions.models import Action


class ActionListView(LoginRequiredMixin, ListView):
    paginate_by = 10
    template_name = 'actions/actions_list.html'

    def get_queryset(self):
        following_ids = self.request.user.following.values_list('id', flat=True)
        return Action.objects.exclude(user=self.request.user).filter(user_id__in=following_ids)[:10]

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['section'] = 'actions'
        return super(ActionListView, self).get_context_data(**kwargs)
