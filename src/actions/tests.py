from django.test import TestCase
from django.urls import reverse

from src.account.models import Post
from src.actions.utils import create_action
from src.authorization.models import CustomUser
from src.base import constants


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
        post = Post.objects.create(owner=user,
                                   title='test_post1',
                                   image=b'',
                                   description='description')

        post2 = Post.objects.create(owner=user2,
                                    title='test_post2',
                                    image=b'',
                                    description='description')
        user.following.add(user2)

        create_action(user, constants.FOLLOWING, user2)
        create_action(user2, constants.LIKES, post)
        create_action(user2, constants.IMAGE, post2)

    def test_action(self):
        login = self.client.login(username='test', password='123456788')
        self.assertTrue(login)
        response = self.client.get(reverse('actions'))
        self.assertEqual(response.context['object_list'].count(), 2)
        self.assertEqual(response.context['section'], 'actions')
        self.assertEqual(response.status_code, 200)
