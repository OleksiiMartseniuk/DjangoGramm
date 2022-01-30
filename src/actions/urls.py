from django.urls import path

from src.actions import views

urlpatterns = [
    # Actions
    path('', views.ActionListView.as_view(), name='actions')
]
