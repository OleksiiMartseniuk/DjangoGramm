from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from src.authorization.models import CustomUser
from src.base import constants
from django.contrib import auth


class AuthenticationTestCase(TestCase):
    def setUp(self) -> None:
        self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
        CustomUser.objects.create_user(username='test',
                                       email='test@test.com',
                                       password='12345678')
        CustomUser.objects.create_user(username='test2',
                                       email='test2@test2.com',
                                       password='123456788',
                                       activ_email=True)

    def test_user_exists(self):
        self.assertEqual(CustomUser.objects.all().count(), 2)

    def test_authentication_email(self, ):
        response = self.client.post(reverse('login'),
                                    data={
                                        'email': 'test2@test2.com',
                                        'password': '123456788',
                                    })
        self.assertEqual(response.status_code, 200)

    def test_login_email(self):
        client = Client()
        self.assertTrue(client.login(username='test2@test2.com', password='123456788'))
        user = auth.get_user(client)
        self.assertTrue(user.is_authenticated)

    def test_not_typical_login_email(self):
        client = Client()
        self.assertFalse(client.login(username='test2@test22.com', password='12223456788'))
        user = auth.get_user(client)
        self.assertFalse(user.is_authenticated)

    def test_registration_user(self):
        response = self.client.post(reverse('register'), data={
            'username': 'test3',
            'email': 'test3@test3.com',
            'password1': '87654321qwqeqwe',
            'password2': '87654321qwqeqwe'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CustomUser.objects.all().count(), 3)
        user = CustomUser.objects.get(username='test3')
        self.assertFalse(user.activ_email)
        uidb = urlsafe_base64_encode(force_bytes(user.username))
        response_profile = self.client.post(reverse('profile_email', kwargs={'uidb64': uidb}),
                                            data={
                                                'first_name': 'Test3',
                                                'last_name': 'Test3'
                                            })
        self.assertEqual(response_profile.status_code, 302)
        self.assertTrue(CustomUser.objects.get(username='test3').activ_email)

    def test_registration_user_form_activ_email_false(self):
        response = self.client.post(reverse('login'),
                                    data={
                                        'username': 'test',
                                        'password': '12345678'
                                    })
        self.assertFormError(response, 'form', None, constants.RAIS_LOGINFORM)
