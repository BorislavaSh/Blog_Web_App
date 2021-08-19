from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User

UserModel = get_user_model()


class SignUpTest(TestCase):
    def setUp(self):
        self.incorrect_data = {
            'username': 'borislava89',
            'email': 'borislavaabv.bg',
            'password1': 'Qwerty789',
            'password2': 'Qwerty789',
        }

    def test_sign_up_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_sign_up_view_post_success(self):
        response = self.client.get(reverse('register'))
        form = response.context['form']
        data = form.initial
        data['username'] = 'borislava45'
        data['email'] = 'borislva@abv.bg'
        data['password1'] = 'Qwerty456'
        data['password2'] = 'Qwerty456'
        response = self.client.post(reverse('register'), data)
        self.assertEqual(User.objects.count(), 1)

    def test_sign_up_view_post_failure(self):
        response = self.client.post(reverse('register'), self.incorrect_data)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertEqual(User.objects.count(), 0)