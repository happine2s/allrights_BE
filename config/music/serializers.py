from rest_framework import serializers
from .models import Music

class MusicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Music
        fields = '__all__'

class MypageMusicSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source = 'author.username')

    class Meta:
        model = Music
        fields = ['title', 'username'] # music_img 필드 추가하기


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

