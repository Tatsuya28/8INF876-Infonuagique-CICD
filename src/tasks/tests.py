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


class Add_task_test(BaseSetUpAfterLogin):

    def test_add_task_page_available(self):
        response = self.client.get(reverse('add_task'))
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
       
        user = User.objects.get(email='test@gmail.com')
        now = timezone.now()


        task_data = {
            'title': 'test_task' ,
            'description':'test_description',
            'due_date':now,
            'user':user
        }

        task= Task.objects.create(**task_data)
        self.assertTrue(Task.objects.filter(title='test_task').exists)

        main_page = self.client.get(reverse('task_list'))
        self.assertContains(main_page, 'test_task')

        task.delete()
        main_page = self.client.get(reverse('task_list'))
        self.assertNotContains(main_page, 'test_task')
    

    def test_create_task_unsuccesful(self):

        usertest = User.objects.get(email='test@gmail.com')
        now = timezone.now()


        task_data = {
            'title': None ,
            'description':None,
            'due_date': None,
            'user':usertest
        }

        
        with self.assertRaises(IntegrityError):
           task= Task.objects.create(**task_data)
        

class BaseSetUpCreateTask(BaseSetUpAfterLogin):

    def setUp(self):

        super().setUp()
        user = User.objects.get(email='test@gmail.com')
        now = timezone.now()


        task_data = {
            'title': 'test_task' ,
            'description':'test_description',
            'due_date':now,
            'user':user
        }

        task= Task.objects.create(**task_data)


class Edit_task_test(BaseSetUpCreateTask):


    def test_access_edit_task(self):

        task_created = Task.objects.get(title='test_task')
        id_task = task_created.pk

        url_with_params = reverse('edit_task') + '?' + urlencode({'task_id': id_task})

        response = self.client.get(url_with_params)

        self.assertEqual(response.status_code, 200)


        self.assertContains(response, 'test_task')
        self.assertContains(response, 'test_description')

    def test_finish_task(self):
        # Récupérer et marquer la tâche comme complétée
        task_created = Task.objects.get(title='test_task')
        task_created.completed = True
        task_created.save()

        # Charger la page de la liste des tâches
        response = self.client.get(reverse('task_list'))

        # Vérifier que le contexte contient les bonnes listes
        self.assertIn('completed_tasks', response.context)
        self.assertIn('uncompleted_tasks', response.context)

        # Vérifier que la tâche complétée est dans la liste correcte
        completed_tasks = response.context['completed_tasks']
        uncompleted_tasks = response.context['uncompleted_tasks']

        self.assertIn(task_created, completed_tasks)
        self.assertNotIn(task_created, uncompleted_tasks)




    def test_edit_task(self):

        task_modified = Task.objects.get(title='test_task')
        task_modified.title = 'test_edit_title'
        task_modified.description= 'test_new_description'
        task_modified.due_date= timezone.now()

        task_modified.save()

        # Charger la page de la liste des tâches
        response = self.client.get(reverse('task_list'))

        # Vérifier que le contexte contient les bonnes listes
        self.assertIn('completed_tasks', response.context)
        self.assertIn('uncompleted_tasks', response.context)

        # Vérifier que la tâche complétée est dans la liste correcte
        completed_tasks = response.context['completed_tasks']
        uncompleted_tasks = response.context['uncompleted_tasks']

        self.assertNotIn(task_modified, completed_tasks)
        self.assertIn(task_modified, uncompleted_tasks)


    def test_bad_edit_task(self):

        bad_task_modified = Task.objects.get(title='test_task')

        bad_task_modified.title= None
        bad_task_modified.due_date= None
        with self.assertRaises(IntegrityError):
            bad_task_modified.save()


class Logout_test(BaseSetUpAfterLogin):

    def test_logout(self):
        session = self.client.session
        self.assertIn('user_id', session)

        response = self.client.get(reverse('logout'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        session = self.client.session
        self.assertNotIn('user_id', session)

