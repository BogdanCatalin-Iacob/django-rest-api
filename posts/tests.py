from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='bogdan', password='pass')
    
    def test_can_list_posts(self):
        bogdan = User.objects.get(username='bogdan')
        Post.objects.create(owner=bogdan, title='a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))
    
    def test_logged_in_user_can_create_post(self):
        self.client.login(username='bogdan', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_logged_out_user_cannot_create_post(self):
        response = self.client.post('/posts/', {'title': 'random title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        bog = User.objects.create_user(username='bog', password='pass')
        cat = User.objects.create_user(username='cat', password='pass')
        Post.objects.create(
            owner=bog, title='random title', content='something extra'
        )
        Post.objects.create(
            owner=cat, title='random 2 title', content='something 2 extra'
        )
    
    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'random title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_user_can_update_own_post(self):
        self.client.login(username='bog', password='pass')
        response = self.client.put('/posts/1/', {'title': 'updated'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'updated')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_not_own_post(self):
        self.client.login(username='bog', password='pass')
        response = self.client.put('/posts/2/', {'title': 'updated'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)