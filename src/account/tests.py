import json
from io import BytesIO
from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from src.account.models import Post
from src.authorization.models import CustomUser


class AccountTestCase(TestCase):
    def setUp(self) -> None:
        user = CustomUser.objects.create_user(username='test',
                                              email='test@test.com',
                                              password='123456788',
                                              activ_email=True)
        user2 = CustomUser.objects.create_user(username='test2',
                                               email='test2@test2.com',
                                               password='1234567882',
                                               activ_email=True)

        user3 = CustomUser.objects.create_user(username='test3',
                                               email='test3@test3.com',
                                               password='1234567883',
                                               activ_email=True)
        Post.objects.create(owner=user,
                            title='test_post',
                            image=b'',
                            description='description')
        Post.objects.create(owner=user,
                            title='test_post',
                            image=b'',
                            description='description')
        Post.objects.create(owner=user2,
                            title='test_post',
                            image=b'',
                            description='description')
        Post.objects.create(owner=user2,
                            title='test_post',
                            image=b'',
                            description='description')
        user.following.add(user2)
        user2.following.add(user)

    def test_home_post_list(self):
        login = self.client.login(username='test', password='123456788')
        self.assertTrue(login)
        response = self.client.get(reverse('home'))
        self.assertTrue(response.context['object_list'])
        self.assertEqual(response.context['section'], 'home')
        self.assertEqual(response.status_code, 200)

    def test_home_recommendations_list(self):
        login = self.client.login(username='test3', password='1234567883')
        self.assertTrue(login)
        response = self.client.get(reverse('home'))
        self.assertFalse(response.context['object_list'])
        self.assertTrue(response.context['recommendations_list'])
        self.assertEqual(response.context['section'], 'home')
        self.assertEqual(response.status_code, 200)

    def test_profile_list(self):
        login = self.client.login(username='test', password='123456788')
        self.assertTrue(login)
        response = self.client.get(reverse('profile', kwargs={'username': 'test'}))
        self.assertEqual(response.context['object_list'].count(), 2)
        self.assertEqual(response.context['user'], CustomUser.objects.get(username='test'))
        self.assertEqual(response.context['section'], 'profile')
        self.assertEqual(response.status_code, 200)

    def test_profile_user_list(self):
        login = self.client.login(username='test', password='123456788')
        self.assertTrue(login)
        response = self.client.get(reverse('profile', kwargs={'username': 'test2'}))
        self.assertEqual(response.context['object_list'].count(), 2)
        self.assertEqual(response.context['user'], CustomUser.objects.get(username='test2'))
        self.assertEqual(response.status_code, 200)

    def test_edit_profile(self):
        login = self.client.login(username='test', password='123456788')
        self.assertTrue(login)
        user = CustomUser.objects.get(username='test')
        self.assertEqual(user.first_name, '')
        response = self.client.post(reverse('profile_edit', kwargs={'username': 'test1'}),
                                    data={
                                        'first_name': 'Test'
                                    })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile', kwargs={'username': 'test'}))
        user = CustomUser.objects.get(username='test')
        self.assertEqual(user.first_name, 'Test')

    def test_subscription_handler_True(self):
        login = self.client.login(username='test', password='123456788')
        self.assertTrue(login)
        user = CustomUser.objects.get(username='test')
        self.assertEqual(user.following.count(), 1)
        response = self.client.post(reverse('subscription'),
                                    data=json.dumps({
                                        'id': CustomUser.objects.get(username='test3').id,
                                        'status': True
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.following.count(), 2)

    def test_subscription_handler_False(self):
        login = self.client.login(username='test', password='123456788')
        self.assertTrue(login)
        user = CustomUser.objects.get(username='test')
        self.assertEqual(user.following.count(), 1)
        response = self.client.post(reverse('subscription'),
                                    data=json.dumps({
                                        'id': CustomUser.objects.get(username='test2').id,
                                        'status': False
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.following.count(), 0)

    def test_followers_delete(self):
        login = self.client.login(username='test', password='123456788')
        self.assertTrue(login)
        user = CustomUser.objects.get(username='test2')
        self.assertEqual(user.following.count(), 1)
        response = self.client.get(reverse('subscription_delete',
                                           kwargs={'user_id': CustomUser.objects.get(username='test2').id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile', kwargs={'username': 'test'}))
        self.assertEqual(user.following.count(), 0)

    # def test_post_create(self):
    #     img = BytesIO(b'mybinarydata')
    #     img.name = 'myimage.png'
    #     login = self.client.login(username='test', password='123456788')
    #     self.assertTrue(login)
    #     user = CustomUser.objects.get(username='test')
    #     self.assertEqual(user.posts.count(), 2)
    #     with open(f'{settings.BASE_DIR}/src/authorization/static/img/images.png', 'rb') as fp:
    #         response = self.client.post(reverse('create_image'),
    #                                     data={
    #                                         'title': 'title_test',
    #                                         'image': fp,
    #                                         'description': 'description',
    #                                     })
    #     user = CustomUser.objects.get(username='test')
    #     print(response.content)
    #     # self.assertEqual(user.posts.count(), 3)
    #     self.assertEqual(response.status_code, 302)
