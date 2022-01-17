from django.urls import path, include

from src.account.views import index, RegistrationUser, ProfileEdit, ToRegistrationUserEmail

urlpatterns = [
    path('', index, name='home'),
    path('', include('django.contrib.auth.urls')),

    path('register/', RegistrationUser.as_view(), name='register'),
    path('register-to-email/', ToRegistrationUserEmail.as_view(), name='register_to_email'),
    path('register/email/<uidb64>', ProfileEdit.as_view(), name='profile_edit'),

]
