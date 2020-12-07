import json, bcrypt

from django.test import TestCase, Client

from unittest.mock import patch, MagicMock
from .models       import User

class SignUpTest(TestCase):

    def setUp(self):
        User.objects.create(
            email = 'testcase1@gmail.com',
            password = bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_user_signup_success(self):
        client = Client()
        new_user = {
            'email' : 'testcase2@gmail.com',
            'password': 'password'
        }

        response = client.post('/user/signup', json.dumps(new_user), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn('access_token', response.json())

    def test_user_signup_failed_invalid_email(self):
        client = Client()
        new_user = {
            'email' : 'thisisnotemail',
            'password': 'password'
        }

        response = client.post('/user/signup', json.dumps(new_user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'INVALID_EMAIL'
            }
        )

    def test_user_signup_failed_invalid_password(self):
        client = Client()
        new_user = {
            'email' : 'testcase3@gmail.com',
            'password': '8char'
        }

        response = client.post('/user/signup', json.dumps(new_user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'INVALID_PASSWORD'
            }
        )

    def test_user_signup_failed_duplicated_email(self):
        client = Client()
        new_user = {
            'email' : 'testcase1@gmail.com',
            'password': 'password123'
        }

        response = client.post('/user/signup', json.dumps(new_user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'DUPLICATED_EMAIL'
            }
        )

    def test_user_signup_failed_keyerror(self):
        client = Client()
        new_user = {
            'email' : 'testcase5@gmail.com',
            'pwd': 'password123'
        }

        response = client.post('/user/signup', json.dumps(new_user), content_type='application/json')

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
        self.assertContains(response, 'access_token')

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

class NaverLoginTest(TestCase):

    def setUp(self):
        test_user = User.objects.create(
            email = 'socialuser1@gmail.com',
            password = bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch('user.views.requests')
    def test_newuser_naver_login_success(self, mocked_request):
        class NaverResponse:
            def json(self):
                return {
                    "resultcode" : "00",
                    "message"    : "success",
                    "response"   : {
                        "email"         : "test@email.com",
                        "nickname"      : "new_user",
                        "profile_image" : "test_image",
                        "age"           : "20-29",
                        "gender"        : "M",
                        "id"            : "12345678",
                        "name"          : "newuser_name",
                        "birthday"      : "05-17"
                    }
                }

        mocked_request.get = MagicMock(return_value = NaverResponse())

        client = Client()
        header = {'HTTP_Authorization': 'naver_token'}
        response = client.post('/user/login/naver', content_type='application/json', **header)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'access_token')

    @patch('user.views.requests')
    def test_existuser_naver_login_success(self, mocked_request):
        class NaverResponse:
            def json(self):
                return {
                    "resultcode" : "00",
                    "message"    : "success",
                    "response"   : {
                        "email"         : "socialuser1@gmail.com",
                        "nickname"      : "exist_user",
                        "profile_image" : "test_image",
                        "age"           : "20-29",
                        "gender"        : "M",
                        "id"            : "12345678",
                        "name"          : "existuser_name",
                        "birthday"      : "05-17"
                    }
                }

        mocked_request.get = MagicMock(return_value = NaverResponse())

        client = Client()
        header = {'HTTP_Authorization': 'naver_token'}
        response = client.post('/user/login/naver', content_type='application/json', **header)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'access_token')

    def test_naver_login_failed_token_missing(self):
        client   = Client()
        header   = {'No_Authorization' : '1234'}
        response = client.post('/user/login/naver', content_type='application/json', **header)

        self.assertEqual(response.status_code, 400)

    @patch('user.views.requests')
    def test_naver_login_failed_invaild_token(self, mocked_request):
        class NaverResponse:
            def json(self):
                return {
                    "resultcode" : "024",
                    "message"    : "Authentication failed (인증 실패하였습니다.)"
                }

        mocked_request.get = MagicMock(return_value = NaverResponse())

        client = Client()
        header = {'HTTP_Authorization': 'invalid_token'}
        response = client.post('/user/login/naver', content_type='application/json', **header)

        self.assertEqual(response.status_code, 400)

class KakaoLoginTest(TestCase):

    def setUp(self):
        test_user = User.objects.create(
            email = 'socialuser1@gmail.com',
            password = bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch('user.views.requests')
    def test_user_kakao_login_success(self, mocked_request):
        class KakaoResponse:
            def json(self):
                return {
                  "id": 12345678,
                  "connected_at": "2020-12-04T09:31:27Z",
                  "properties": {
                    "nickname": "kakaotest",
                    "profile_image": "testuser_profile",
                    "thumbnail_image": "testuser_thumbnail"
                  },
                  "kakao_account": {
                    "profile_needs_agreement": 'false',
                    "profile": {
                      "nickname": "kakaotest",
                      "thumbnail_image_url": "testuser_thumbnail",
                      "profile_image_url": "testuser_profile"
                    },
                    "has_email": 'true',
                    "email_needs_agreement": 'false',
                    "is_email_valid": 'true',
                    "is_email_verified": 'true',
                    "email": "test@email",
                    "has_age_range": 'true',
                    "age_range_needs_agreement": 'false',
                    "age_range": "20~29",
                    "has_birthday": 'true',
                    "birthday_needs_agreement": 'false',
                    "birthday": "0517",
                    "birthday_type": "SOLAR",
                    "has_gender": 'true',
                    "gender_needs_agreement": 'false',
                    "gender": "male"
                  }
                }

        mocked_request.get = MagicMock(return_value = KakaoResponse())

        client = Client()
        header = {'HTTP_Authorization': 'kakao_token'}
        response = client.post('/user/login/kakao', content_type='application/json', **header)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'access_token')

    def test_kakao_login_failed_token_missing(self):
        client   = Client()
        header   = {'No_Authorization' : '1234'}
        response = client.post('/user/login/kakao', content_type='application/json', **header)

        self.assertEqual(response.status_code, 400)

class GoogleLoginTest(TestCase):

    def setUp(self):
        test_user = User.objects.create(
            email = 'socialuser1@gmail.com',
            password = bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch('user.views.requests')
    def test_user_google_login_success(self, mocked_request):
        class GoogleResponse:
            def json(self):
                return {
                    "picture": "test_picture",
                    "verified_email": 'true',
                    "id": "123456789098765432123",
                    "email": "testuser@gmail.com"
                }

        mocked_request.get = MagicMock(return_value = GoogleResponse())

        client = Client()
        header = {'HTTP_Authorization': 'google_token'}
        response = client.post('/user/login/google', content_type='application/json', **header)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'access_token')

    def test_google_login_failed_token_missing(self):
        client   = Client()
        header   = {'No_Authorization' : '1234'}
        response = client.post('/user/login/google', content_type='application/json', **header)

        self.assertEqual(response.status_code, 400)
