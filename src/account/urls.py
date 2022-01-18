from django.urls import path

from src.account.views import index, ProfileListView

urlpatterns = [
    path('', index, name='home'),
    path('profile/<slug:username>/', ProfileListView.as_view(), name='profile')
]
