from django.urls import path, include
from .views import *

urlpatterns = [
    path('signup/',signup.as_view()),
    path('signin/',signin.as_view()),
    path('signout/',signout.as_view()),
    path('password/',update_password.as_view()),
]
