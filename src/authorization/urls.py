from django.urls import path

from src.authorization.forms import LoginForm
from django.contrib.auth import views as auth_views
from src.authorization.views import RegistrationUser, ProfileEdit, ToRegistrationUserEmail

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Шаблоны для доступа к обработчикам смены пароля
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # Обработчики восстановления пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('register/', RegistrationUser.as_view(), name='register'),
    path('register-to-email/', ToRegistrationUserEmail.as_view(), name='register_to_email'),
    path('register/email/<uidb64>', ProfileEdit.as_view(), name='profile_email'),

]
