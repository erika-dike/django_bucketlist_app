"""Import test tools from rest_framework."""
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class APIAccessTestCAse(APITestCase):
    """Tests for API authorization"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='itachi',
                                             password='lifidum')

    def test_user_can_register(self):
        credentials = {'username': 'rikky', 'password': 'rikky'}
        url = reverse_lazy('user-register')
        response = self.client.post(url, credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_login(self):
        response = self.client.login(username='itachi', password='lifidum')
        self.assertEqual(response, True)

    def test_user_gets_token_with_post_signin(self):
        credentials = {'username': 'itachi', 'password': 'lifidum'}
        url = reverse_lazy('user-login')
        response = self.client.post(url, credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.json())

    def test_user_can_not_view_bucketlist_without_authentication(self):
        url = reverse_lazy('bucketlist-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
