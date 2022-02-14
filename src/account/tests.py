import json
from django.test import TestCase
from django.urls import reverse

from src.account.models import Post, Comment
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
        post = Post.objects.create(owner=user,
                                   title='test_post',
                                   image=b'',
                                   description='description')
        Post.objects.create(owner=user,
                            title='test_post1',
                            image=b'',
                            description='description')
        Post.objects.create(owner=user2,
                            title='test_post2',
                            image=b'',
                            description='description')
        Post.objects.create(owner=user2,
                            title='test_post3',
                            image=b'',
                            description='description')
        Comment.objects.create(owner=user,
                               post=post,
                               text='text')
        user.following.add(user2)
        user2.following.add(user)

        post.like.add(user)
        self.login = self.client.login(username='test', password='123456788')

    def test_home_post_list(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse('home'))
        self.assertTrue(response.context['object_list'])
        self.assertEqual(response.context['section'], 'home')
        self.assertEqual(response.status_code, 200)

    def test_home_recommendations_list(self):
        self.client.logout()
        login = self.client.login(username='test3', password='1234567883')
        self.assertTrue(login)
        response = self.client.get(reverse('home'))
        self.assertFalse(response.context['object_list'])
        self.assertTrue(response.context['recommendations_list'])
        self.assertEqual(response.context['section'], 'home')
        self.assertEqual(response.status_code, 200)

    def test_profile_list(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse('profile', kwargs={'username': 'test'}))
        self.assertEqual(response.context['object_list'].count(), 2)
        self.assertEqual(response.context['user'], CustomUser.objects.get(username='test'))
        self.assertEqual(response.context['section'], 'profile')
        self.assertEqual(response.status_code, 200)

    def test_profile_user_list(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse('profile', kwargs={'username': 'test2'}))
        self.assertEqual(response.context['object_list'].count(), 2)
        self.assertEqual(response.context['user'], CustomUser.objects.get(username='test2'))
        self.assertEqual(response.status_code, 200)

    def test_edit_profile(self):
        self.assertTrue(self.login)
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
        self.assertTrue(self.login)
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
        self.assertTrue(self.login)
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
        self.assertTrue(self.login)
        user = CustomUser.objects.get(username='test2')
        self.assertEqual(user.following.count(), 1)
        response = self.client.get(reverse('subscription_delete',
                                           kwargs={'user_id': CustomUser.objects.get(username='test2').id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile', kwargs={'username': 'test'}))
        self.assertEqual(user.following.count(), 0)

    def test_post_delete(self):
        self.assertTrue(self.login)
        user = CustomUser.objects.get(username='test')
        self.assertEqual(Post.objects.filter(owner=user).count(), 2)
        response = self.client.get(reverse('delete_image',
                                           kwargs={'pk': Post.objects.filter(owner=user).first().id}))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('delete_image',
                                                kwargs={'pk': Post.objects.filter(owner=user).first().id}))
        self.assertRedirects(post_response, reverse('profile', kwargs={'username': 'test'}))
        self.assertEqual(Post.objects.filter(owner=user).count(), 1)

    def test_image_detail(self):
        self.assertTrue(self.login)
        user = CustomUser.objects.get(username='test')
        post = Post.objects.filter(owner=user).first()
        comment = Comment.objects.filter(post=post)
        self.assertEqual(comment.count(), 1)
        response = self.client.get(reverse('detail_image', kwargs={'slug': post.slug}))
        self.assertEqual(response.context['comments_list'].count(), 1)
        self.assertEqual(response.context['object'], post)
        self.assertEqual(response.status_code, 200)

    def test_like_image_handler(self):
        self.assertTrue(self.login)
        post = Post.objects.get(title='test_post')
        self.assertEqual(post.like.count(), 1)
        response = self.client.post(reverse('like'),
                                    data=json.dumps({
                                        'id': post.id,
                                        'action': 'unlike',
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.like.count(), 0)
        response = self.client.post(reverse('like'),
                                    data=json.dumps({
                                        'id': post.id,
                                        'action': 'like',
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.like.count(), 1)
        response = self.client.post(reverse('like'),
                                    data=json.dumps({
                                        'id': 6,
                                        'action': 'unlike',
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.like.count(), 1)

    def test_comment_delete(self):
        self.assertTrue(self.login)
        user = CustomUser.objects.get(username='test')
        self.assertEqual(Comment.objects.filter(owner=user).count(), 1)
        comment = Comment.objects.filter(owner=user).first()
        response = self.client.get(reverse('delete_comment', kwargs={'pk': comment.id}))
        self.assertEqual(response.status_code, 200)

        response_post = self.client.post(reverse('delete_comment', kwargs={'pk': comment.id}))
        post = Post.objects.get(title='test_post')
        self.assertRedirects(response_post, reverse('detail_image', kwargs={'slug': post.slug}))
        self.assertEqual(Comment.objects.filter(owner=user).count(), 0)
