from django.urls import path

from src.account import views

urlpatterns = [
    path('', views.index, name='home'),
    path('profile/subscription/', views.SubscriptionHandler.as_view(), name='subscription'),
    path('profile/subscription/delete/<int:user_id>/', views.FollowersHandler.as_view(), name='subscription_delete'),
    path('profile/<slug:username>/', views.ProfileListView.as_view(), name='profile'),
    path('profile/edit/<slug:username>/', views.EditProfileUpdateView.as_view(), name='profile_edit'),
    path('image/like/', views.LikeImageHandler.as_view(), name='like'),
    path('image/create/', views.PostCreateView.as_view(), name='create_image'),
    path('image/<slug:slug>/', views.ImageDetailView.as_view(), name='detail_image'),
    path('delete/image/<int:pk>/', views.PostDeleteView.as_view(), name='delete_image'),
    path('delete/comment/<int:pk>/', views.CommentDeleteView.as_view(), name='delete_comment'),
]
