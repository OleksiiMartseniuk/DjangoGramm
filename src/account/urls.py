from django.urls import path

from src.account.views import index

urlpatterns = [
    path('', index, name='home'),
]
