from django.urls import path

from .views import UserView, LoginView, NaverLoginView, KakaoLoginView, GoogleLoginView

urlpatterns = [
    path('/signup', UserView.as_view()),
    path('/login', LoginView.as_view()),
    path('/login/naver', NaverLoginView.as_view()),
    path('/login/kakao', KakaoLoginView.as_view()),
    path('/login/google', GoogleLoginView.as_view())
]
