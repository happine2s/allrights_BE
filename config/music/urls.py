from django.urls import path
from .views import MusicList, MusicDetail

urlpatterns = [
    path('', MusicList.as_view()),
    path('<int:pk>/', MusicDetail.as_view()),
]
