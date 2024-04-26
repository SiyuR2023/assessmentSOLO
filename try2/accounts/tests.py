from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserLoginTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        User.objects.create_user(**self.credentials)

    def test_login_with_correct_credentials(self):
        response = self.client.post(reverse('user_login'), self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)


class UserRegisterTest(TestCase):
    def test_register_with_valid_data(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        response = self.client.post(reverse('register'), form_data, follow=True)
        # Verify that the user has been created
        self.assertTrue(User.objects.filter(username='newuser').exists())
        # Verify that it redirects to the login page
        self.assertRedirects(response, reverse('user_login'))

class CartTest(TestCase):
    def setUp(self):
        Album.objects.create(id=1, title="Test Album", artist="Artist", genre="Rock")
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_add_to_cart(self):
        response = self.client.post(reverse('add_to_cart', kwargs={'album_id': 1}))
        self.assertIn(1, self.client.session['cart'])
        self.assertRedirects(response, reverse('cart'))
