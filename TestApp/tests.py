from django.test import TestCase, Client
from .models import User


class TestHome(TestCase):
    def setUp(self):
        self.c = Client()

    def test_home(self):
        response = self.c.post('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'empty')

        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'empty')


    ####################
    # HTML sample:
    ####################
    #
    # <form method="post" action="/" id="inputform">
    #
    ####################

class TestAddUser(TestCase):
    def setUp(self):
        self.c = Client()

    def test_form_client(self):
        self.c.post('/add_user/', {'first_name': 'Andrew', 'last_name': 'Hughes', 'username': 'Hughes1'})

        self.assertEqual(len(User.objects.all()), 1, 'Err: no user made')
        self.assertEqual(User.objects.all()[0].first_name, 'Andrew', 'Err: user attribute failure 0')
        self.assertEqual(User.objects.get(first_name='Andrew').username, 'Hughes1', 'Err: user attribute failure 1')
        self.assertEqual(User.objects.get(username='Hughes1').first_name, 'Andrew', 'Err: user attribute failure 2')
        self.assertEqual(User.objects.get(username='Hughes1').first_name, 'Andrew', 'Err: user attribute failure 3')

    def test_form_fails(self):
        response = self.c.post('/add_user/', {'first_name': 'Andrew', 'last_name': 'Hughes'})
        self.assertEqual(len(User.objects.all()), 0, 'Err: user made 1')
        self.assertFalse(response.context['form'].is_valid(), 'Err: invalid form marked valid a')
        print(response.context['form'])
        print('\n')

        response = self.c.post('/add_user/', {'first_name': 'Andrew', 'username': 'Hughes1'})
        self.assertFalse(response.context['form'].is_valid(), 'Err: invalid form marked valid b')
        self.assertEqual(len(User.objects.all()), 0, 'Err: user made 2')
        print(response.context['form'])
        print('\n')

        response = self.c.post('/add_user/', {'last_name': 'Hughes', 'username': 'Hughes1'})
        self.assertEqual(len(User.objects.all()), 0, 'Err: user made 3')
        self.assertFalse(response.context['form'].is_valid(), 'Err: invalid form marked valid c')
        print(response.context['form'])


class TestAssignFriends(TestCase):
    def setUp(self):
        self.c = Client()
        self.c.post('/add_user/', {'first_name': 'Andrew', 'last_name': 'Hughes', 'username': 'Hughes1'})
        self.username_a = 'Hughes1'
        self.user_a = User.objects.get(username='Hughes1')

        self.username_b = 'Hughes2'
        self.username_c = 'Wheezy'
        self.user_b = User(first_name='Burt', last_name='Hughes', username='Hughes2')
        self.user_b.save()
        self.user_c = User(first_name='Carl', last_name='Wheezer', username='Wheezy')
        self.user_c.save()

    def test_proper_assign(self):
        self.c.post('/add_friend/', {'username_a': self.username_a, 'username_b': self.username_b})

        self.assertEqual(len(self.user_a.friends.all()), 1, 'Err: friend not added one way')
        self.assertEqual(len(self.user_b.friends.all()), 1, 'Err: friend not added the other')
        self.assertEqual(len(self.user_c.friends.all()), 0, 'Err: Carl has a friend')
        self.assertEqual(self.user_a.friends.get(username='Hughes2'), self.user_b, 'Err: user b is not a real friend')
        self.assertEqual(self.user_b.friends.get(username='Hughes1'), self.user_a, 'Err: user a is not a real friend')

    def test_same_assign(self):
        response = self.c.post('/add_friend/', {'username_a': self.username_a, 'username_b': self.username_a})
        self.assertEqual(len(self.user_a.friends.all()), 0, 'Err: I have a friend')
        self.assertFalse(response.context['form'].is_valid(), 'Err: friended oneself')

    def test_bad_form(self):
        response = self.c.post('/add_friend/', {'username_a': self.username_a})
        self.assertEqual(len(self.user_a.friends.all()), 0, 'Err: Faulty args 1')
        self.assertFalse(response.context['form'].is_valid(), 'Err: Faulty args a')

        response = self.c.post('/add_friend/', {'username_b': self.username_a})
        self.assertEqual(len(self.user_a.friends.all()), 0, 'Err: Faulty args 2')
        self.assertFalse(response.context['form'].is_valid(), 'Err: Faulty args b')


