from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from src.authorization.models import CustomUser


class AuthenticationTestCase(TestCase):
    def setUp(self) -> None:
        CustomUser.objects.create_user(username='test',
                                       email='test@test.com',
                                       password='12345678')

    def test_user_exists(self):
        self.assertEqual(CustomUser.objects.all().count(), 1)

    def test_authentication_email(self, ):
        client = Client()
        logged_in = client.login(username='test@test.com', password='12345678')
        self.assertTrue(logged_in)

    def test_registration_user_form(self):
        with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            response = self.client.post(reverse('register'), data={
                'username': 'test1',
                'email': 'test1@test1.com',
                'password1': '87654321qwqeqwe',
                'password2': '87654321qwqeqwe'
            })
            self.assertEqual(response.status_code, 302)
            self.assertEqual(CustomUser.objects.all().count(), 2)
            user = CustomUser.objects.get(username='test1')
            self.assertFalse(user.activ_email)
            uidb = urlsafe_base64_encode(force_bytes(user.username))
            response_profile = self.client.post(reverse('profile_email', kwargs={'uidb64': uidb}),
                                                data={
                                                    'first_name': 'Test',
                                                    'last_name': 'Test1'
                                                })
            self.assertEqual(response_profile.status_code, 302)
            self.assertTrue(CustomUser.objects.get(username='test1').activ_email)


