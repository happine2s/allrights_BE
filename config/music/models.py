import os
from django.db import models
from django.utils import timezone
from account.models import User
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen import File as MutagenFile


class Music(models.Model):
    MUSIC_TYPES = (
        ('effect', '효과음'),
        ('background', '배경음악'),
    )

    GENRE_TYPES = (
        ('hiphop', '힙합'),
        ('rock', '락'),
        ('pop', '팝'),
        ('jazz', '재즈'),
        ('classic', '클래식'),
        ('blues', '블루스'),
        ('fork', '포크'),
        ('indie', '인디'),
        ('rnb', 'R&B'),
    )

    MOOD_TYPES = (
        ('depressed', '우울한'),
        ('excited', '신나는'),
        ('happy', '쾌활한'),
        ('peaceful', '평화로운'),
        ('serious', '심각한'),
        ('urgent', '급박한'),
        ('horrifying', '소름 끼치는'),
    )

    INSTRUMENTS_TYPES = (
        ('piano', '피아노'),
        ('acoustic guitar', '어쿠스틱 기타'),
        ('bass', '베이스'),
        ('drum', '드럼'),
        ('violin', '바이올린'),
    )

    title = models.CharField(max_length=100)
    music_file = models.FileField(upload_to='music/')
    music_type = models.CharField(max_length=100, choices=MUSIC_TYPES)
    genre = models.CharField(max_length=100, choices=GENRE_TYPES)
    instruments = models.CharField(max_length=100, choices=INSTRUMENTS_TYPES)
    mood = models.CharField(max_length=100, choices=MOOD_TYPES)
    length = models.FloatField(null=True, blank=True)
    description = models.TextField()
    upload_date = models.DateTimeField(default=timezone.now)  # 업로드 날짜 및 시간
    downloads = models.PositiveIntegerField(default=0)  # 다운로드 횟수

    music_image = models.ImageField(upload_to='image/', blank=True)

    # def save(self, *args, **kwargs):
    #     if not self.length and self.music_file:
    #         file_extension = os.path.splitext(self.music_file.name)[1].lower()
    #         audio = MutagenFile(self.music_file.path)
            
    #         if file_extension == '.mp3':
    #             self.length = audio.info.length
    #         elif file_extension == '.m4a':
    #             self.length = audio.info.length
    #         # 다른 오디오 형식을 처리하려면 여기에 추가
            
    #     super(Music, self).save(*args, **kwargs)

    author=models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    liker=models.ManyToManyField(User,related_name='like_music',default=[],blank=True)

    def save(self, *args, **kwargs):
        if not self.length and self.music_file:
            audio = MP4(self.music_file.path)
            self.length = audio.info.length
        super(Music, self).save(*args, **kwargs)


