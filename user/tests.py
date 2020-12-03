import json, bcrypt, jwt

from django.test import TestCase, Client

from .models import User
from my_settings import SECRET_KEY, ALGORITHM

class UserTest(TestCase):

    def setUp(self):
        User.objects.create(
            email = 'testcase1@gmail.com',
            password = bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_userview_post_success(self):
        client = Client()
        new_user = {
            'email' : 'testcase2@gmail.com',
            'password': 'password'
        }

        response = client.post('/user', json.dumps(new_user), content_type='application/json')

        self.assertEqual(response.status_code, 201)

    def test_userview_post_invalid_email(self):
        client = Client()
        new_user = {
            'email' : 'thisisnotemail',
            'password': 'password'
        }

        response = client.post('/user', json.dumps(new_user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'INVALID_EMAIL'
            }
        )

    def test_userview_post_invalid_password(self):
        client = Client()
        new_user = {
            'email' : 'testcase3@gmail.com',
            'password': '8char'
        }

        response = client.post('/user', json.dumps(new_user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'INVALID_PASSWORD'
            }
        )

    def test_userview_post_duplicated_email(self):
        client = Client()
        new_user = {
            'email' : 'testcase1@gmail.com',
            'password': 'password123'
        }

        response = client.post('/user', json.dumps(new_user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'DUPLICATED_EMAIL'
            }
        )

    def test_userview_post_keyerror(self):
        client = Client()
        new_user = {
            'email' : 'testcase5@gmail.com',
            'pwd': 'password123'
        }

        response = client.post('/user', json.dumps(new_user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR'
            }
        )

class LoginTest(TestCase):

    def setUp(self):
        test_user = User.objects.create(
            email = 'logintest1@gmail.com',
            password = bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )
        self.test_token = jwt.encode({'id':test_user.id}, SECRET_KEY, algorithm=ALGORITHM).decode('utf-8')


    def tearDown(self):
        User.objects.all().delete()

    def test_loginview_post_success(self):
        client = Client()
        login_user = {
            'email' : 'logintest1@gmail.com',
            'password' : 'password'
        }

        response = client.post('/user/login', json.dumps(login_user), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message' : 'SUCCESS',
                'access_token' : self.test_token
            }
        )

    def test_loginview_post_wrong_password(self):
        client = Client()
        login_user = {
            'email' : 'logintest1@gmail.com',
            'password' : 'passw0rd'
        }

        response = client.post('/user/login', json.dumps(login_user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'INVALID_EMAIL_OR_PASSWORD'
            }
        )

    def test_loginview_post_not_exist_user(self):
        client = Client()
        login_user = {
            'email' : 'doesnotexist@gmail.com',
            'password' : 'passw0rd'
        }

        response = client.post('/user/login', json.dumps(login_user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'INVALID_EMAIL_OR_PASSWORD'
            }
        )

    def test_loginview_post_keyerror(self):
        client = Client()
        login_user = {
            'email' : 'doesnotexist@gmail.com',
            'pwd' : 'passw0rd'
        }

        response = client.post('/user/login', json.dumps(login_user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR'
            }
        )
