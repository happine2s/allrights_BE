from rest_framework import serializers
from .models import Music

class MusicSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    class Meta:
        model = Music
        fields = '__all__'
    