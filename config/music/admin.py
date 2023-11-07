from django.contrib import admin
from .models import Music

@admin.register(Music)
class MusicModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'music_type', 'length', 'upload_date', 'downloads']