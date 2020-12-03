import jwt, json

from django.http import JsonResponse

from my_settings import SECRET_KEY, ALGORITHM
from user.models import User

def login_check(func):

    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload      = jwt.decode(access_token, SECRET_KEY, algorithm=ALGORITHM)
            request.user = User.objects.get(id=payload['id'])

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID TOKEN'}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID USER'}, status = 400)

        return func(self, request, *args, **kwargs)

    return wrapper
