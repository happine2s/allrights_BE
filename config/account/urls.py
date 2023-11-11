from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view()), # jwt 재발급
    path('signup/',signup.as_view()),
    path('auth/',auth.as_view()),
    path('signin/',signin.as_view()),
    path('signout/',signout.as_view()),
    path('password/<int:user_pk>/',update_password.as_view()),
    path('mypage/<int:user_pk>/',mypage.as_view()),
    path('mypage/update/<int:user_pk>/',update_mypage.as_view()),
]
