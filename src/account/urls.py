from django.urls import path

from src.account.views import index, ProfileListView, ImageDetailView

urlpatterns = [
    path('', index, name='home'),
    path('profile/<slug:username>/', ProfileListView.as_view(), name='profile'),
    path('image/<slug:slug>/', ImageDetailView.as_view(), name='detail_image'),
]
