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


class MypageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userid', 'username', 'password','img','bio']
    
    password = serializers.CharField(write_only=True)
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance