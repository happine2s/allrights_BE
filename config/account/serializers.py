from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userid', 'username', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            userid = validated_data['userid'],
            username = validated_data['username'],
            password=validated_data['password']
        )

        return user
