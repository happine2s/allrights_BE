from django.urls import path
from .views import MusicList, MusicDetail, MusicSearch

urlpatterns = [
    path('', MusicList.as_view()),
    path('<int:pk>/', MusicDetail.as_view()),
    path('search/', MusicSearch.as_view(), name='music-search'),
]
