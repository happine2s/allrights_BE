from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','userid', 'username', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            userid = validated_data['userid'],
            username = validated_data['username'],
            password=validated_data['password']
        )

        return user


class UpdateMypageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','userid', 'username', 'password','img','bio']
    
    password = serializers.CharField(write_only=True)
    
    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


# class UpdatePasswordSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=User
#         fields=['id','userid','password']
    
#     password=serializers.CharField(write_only=True)


class MypageUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','userid', 'username', 'img','bio']
