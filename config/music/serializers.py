from rest_framework import serializers
from .models import Music

class MusicSerializer(serializers.ModelSerializer):
    username=serializers.SerializerMethodField()

    def get_username(self, obj):
        try:
            if obj.author.username:
                return obj.author.username
        except:
                return 'anonymous'

    class Meta:
        model = Music
        fields = '__all__'


class MypageMusicSerializer(serializers.ModelSerializer):
    username=serializers.SerializerMethodField()

    def get_username(self, obj):
        try:
            if obj.author.username:
                return obj.author.username
        except:
                return 'anonymous'
    
    class Meta:
        model = Music
        fields = ['id', 'title', 'username','music_image','music_file'] # music_img 필드 추가하기


class LikeMusicSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    liker = serializers.StringRelatedField(many=True)

    def get_author(self, obj):
        try:
            if obj.author.username:
                return obj.author.username
        except:
                return 'anonymous'

    class Meta:
        model = Music
        fields = ("id", "author", 'liker')

