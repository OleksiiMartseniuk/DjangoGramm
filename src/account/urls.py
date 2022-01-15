from django.urls import path, include

from src.account.views import index

urlpatterns = [
    path('', index, name='index'),
    path('', include('django.contrib.auth.urls')),
]
