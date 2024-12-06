from urllib.parse import urlencode
from django.utils import timezone
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from tasks.models import User, Task

# Create your tests here.


class Register_test(TestCase):
    
    def test_register_page_exists(self):
        """
        Vérifier la disponibilité de la page register
        """
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/register.html')

    def test_register(self):
        """
        Vérifier que l'utilisateur est créé après l'inscription
        """
        user_data = {
            'name': 'test_user',
            'email': 'test@gmail.com',
            'password': 'test_password',
            'confirm_password': 'test_password',
        }
        response = self.client.post(reverse('register'), user_data, format='text/html')
        
        # Vérifier que la réponse redirige après la création (code 302)
        self.assertEqual(response.status_code, 302)
        
        # Vérifier que l'utilisateur est bien créé dans la base de données
        user_exists = User.objects.filter(email='test@gmail.com').exists()
        self.assertTrue(user_exists)




class BaseSetUp(TestCase):
   def setUp(self):
    user_data = {
            'name' : 'test_user',
            'email' : 'test@gmail.com',
            'password' : 'test_password',
            'confirm_password' : 'test_password',
        }
    response = self.client.post(reverse('register'), user_data, format='text/html')

    


class Login_test(BaseSetUp):
    
    def test_login_page_exists(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/login.html')

    def test_login(self):
        user_data = {
            'email' : 'test@gmail.com',
            'password' : 'test_password',
        }
        response = self.client.post(reverse('login'), user_data, format='text/html')
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, reverse('task_list'))



class BaseSetUpAfterLogin(TestCase):
   def setUp(self):
    user_data = {
            'name' : 'test_user',
            'email' : 'test@gmail.com',
            'password' : 'test_password',
            'confirm_password' : 'test_password',
        }
    response = self.client.post(reverse('register'), user_data, format='text/html')

    response = self.client.post(reverse('login'), user_data, format='text/html')
    self.assertEqual(response.status_code, 302)

    self.assertRedirects(response, reverse('task_list'))


