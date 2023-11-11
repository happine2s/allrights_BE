from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import MusicList, MusicDetail, MusicSearch, download_music
from .views import *

urlpatterns = [
    path('', MusicList.as_view()),
    path('<int:pk>/', MusicDetail.as_view()),
    path('search/', MusicSearch.as_view(), name='music-search'),
    path('download/<int:music_id>/', download_music, name='download-music'),
    path('like/<int:music_pk>/',LikeMusic.as_view()),
    #path('length/', MusicLengthUpdate.as_view(), name='music-length'),
]