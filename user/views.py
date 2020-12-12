import re, json, bcrypt, jwt, requests, random, datetime

from django.views import View
from django.http import JsonResponse

from user.models import User, UserDetail, PhoneAuth
from .utils      import login_check, generate_token
from .api_urls   import NAVER_API, KAKAO_API, GOOGLE_API
from my_settings import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email    = data['email']
            password = data['password']

            email_validation = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

            if not re.match(email_validation, email):
                return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)

            if len(password) < 8:
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'DUPLICATED_EMAIL'}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            user = User.objects.create(
                email    = email,
                password = hashed_password
            )

            access_token = generate_token(user)

            return JsonResponse({'message': 'SUCCESS', 'access_token': access_token}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email    = data['email']
            password = data['password']

            user = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message': 'INVALID_EMAIL_OR_PASSWORD'}, status=400)

            access_token =  generate_token(user)

            return JsonResponse({'message': 'SUCCESS', 'access_token': access_token}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_EMAIL_OR_PASSWORD'}, status=400)

class NaverLoginView(View):
    def post(self, request):
        naver_token = request.headers.get('Authorization', None)
        token_type  = 'Bearer'

        if not naver_token:
            return JsonResponse({'message': 'TOKEN_REQUIRED'}, status=400)

        result = requests.get(
            NAVER_API,
            headers = {
                'Authorization' : '{} {}'.format(token_type, naver_token)
            }
        ).json()

        if result.get('resultcode') != '00':
            return JsonResponse({'message': result.get('message')}, status=400)

        if not 'email' in result.get('response'):
            return JsonResponse({'message': 'EMAIL_REQUIRED'}, status=405)

        data = result.get('response')

        user, flag   = User.objects.get_or_create(email=data['email'])
        access_token = generate_token(user)

        return JsonResponse({'message': 'SUCCESS', 'access_token': access_token}, status=200)

class KakaoLoginView(View):
    def post(self, request):
        kakao_token = request.headers.get('Authorization', None)
        token_type  = 'Bearer'

        if not kakao_token:
            return JsonResponse({'message': 'TOKEN_REQUIRED'}, status=400)

        response = requests.get(
            KAKAO_API,
            headers = {
                'Authorization' : '{} {}'.format(token_type, kakao_token)
            }
        ).json()

        if not 'email' in response['kakao_account']:
            return JsonResponse({'message': 'EMAIL_REQUIRED'}, status=405)

        user, flag   = User.objects.get_or_create(email=response['kakao_account']['email'])
        access_token = generate_token(user)

        return JsonResponse({'message': 'SUCCESS', 'access_token': access_token}, status=200)

class GoogleLoginView(View):
    def post(self, request):
        google_token = request.headers.get('Authorization', None)
        token_type   = 'Bearer'

        if not google_token:
            return JsonResponse({'message': 'TOKEN_REQUIRED'}, status=400)

        response = requests.get(
            GOOGLE_API,
            headers = {
                'Authorization' : '{} {}'.format(token_type, google_token)
            }
        ).json()

        if not 'email' in response:
            return JsonResponse({'message': 'EMAIL_REQUIRED'}, status=405)

        user, flag   = User.objects.get_or_create(email=response['email'])
        access_token = generate_token(user)

        return JsonResponse({'message': 'SUCCESS','access_token': access_token}, status=200)

class UserDetailView(View):
    @login_check
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user

            DATE_FORMAT = "%Y-%m-%d"
            datetime.datetime.strptime(data['dob'], DATE_FORMAT)

            PhoneAuth.objects.get(phone=data['phone'], auth_number=data['auth_number'])

            UserDetail.objects.update_or_create(
                defaults = {
                    'name'   : data['name'],
                    'phone'  : data['phone'],
                    'dob'    : data['dob'],
                    'gender' : data['gender']
                },
                user = user
            )

            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except PhoneAuth.DoesNotExist:
            return JsonResponse({'message': 'PHONE_AUTHENTICATION_FAILED'}, status=401)

        except ValueError:
            return JsonResponse({'message': 'DATE_FORMAT_SHOULD_BE_YYYY-MM-DD'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class PhoneAuthView(View):
    def post(self, request):
        try:
            data        = json.loads(request.body)
            auth_number = random.randint(10000,100000)

            phone_auth, _ = PhoneAuth.objects.update_or_create(
                defaults = {'auth_number' : auth_number},
                phone    = data['phone']
            )

            result = phone_auth.send_message()

            if not 'statusCode' in result:
                return JsonResponse({'message': 'FAIL', 'result': result}, status=405)

            if result['statusCode'] != '202':
                return JsonResponse({'message': result['statusName']}, status=result['statusCode'])

            return JsonResponse({'message': 'SUCCESS'}, status=202)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
