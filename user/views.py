import re, json, bcrypt, jwt

from django.views import View
from django.db.models import Q
from django.http import JsonResponse

from user.models import User, UserDetail
from my_settings import SECRET_KEY, ALGORITHM

class UserView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email = data['email']
            password = data['password']

            email_validation = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

            if not re.match(email_validation, email):
                return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)

            if len(password) < 8:
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'DUPLICATED_EMAIL'}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                email = email,
                password = hashed_password
            )

            return JsonResponse({'message': 'SUCCESS'}, status=201)

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

            access_token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=ALGORITHM).decode('utf-8')

            return JsonResponse({'message': 'SUCCESS', 'access_token': access_token}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_EMAIL_OR_PASSWORD'}, status=400)
