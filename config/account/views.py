from django.shortcuts import render
from .models import User
from .serializers import *
from music.models import Music
from music.serializers import MusicSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.http import Http404


class signup(APIView):
    def post(self, request):
        serializer=UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            data={
                "msg":"created",
                "user_info": serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)

        else:
            data={
                "msg":"failed"
            }
            return Response(data, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class signin(APIView):
    def post(self, request):
        userid=request.data['userid']
        password=request.data['password']
        user=authenticate(request,userid=userid, password=password)

        if user is not None:
            auth.login(request,user)
            data={
                "msg":"ok",
                "userid":userid
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            # 로그인 실패 시
            data={
                "msg":"failed"
            }
            return Response(data,status=status.HTTP_404_NOT_FOUND)

class signout(APIView):
    def post(self, request):
        auth.logout(request)
        data={
            "msg":"ok"
        }
        return Response(data, status=status.HTTP_200_OK)

class update_password(APIView):
    def post(self, request):
        user=request.user
        origin_password=request.data['origin_password']

        if check_password(origin_password,user.password):
            password1=request.data["password1"]
            password2=request.data["password2"]

            if password1==password2:
                user.set_password(password1)
                user.save()
                auth.login(request,user)
                data={
                    "msg":"ok"
                }
                return Response(data,status=status.HTTP_202_ACCEPTED)
            else:
                data={
                    "msg":"비밀번호가 일치하지 않습니다."
                }
                return Response(data,status=status.HTTP_406_NOT_ACCEPTABLE)
        
        else:
            data={
                    "msg":"기존 비밀번호가 알맞지 않습니다."
                }
            return Response(data,status=status.HTTP_401_UNAUTHORIZED)

class update_mypage(APIView): # 로그인한 사용자의 정보 수정
    permission_classes = (IsAuthenticated,)
    serializer_class = MypageSerializer

    def put(self, request): # 비밀번호는 변경 안됨
        serializer_data = request.data
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class mypage(APIView): # url의 user_pk에 대한 마이페이지
    def get_object(self, user_pk):
        try:
            return User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, user_pk):
        try:
            user = self.get_object(user_pk)
            serializer = UserSerializer(user)
            data={
                "user_info":serializer.data,
            }
            return Response(data, status=status.HTTP_200_OK)
        except:
            data={
                "msg":"일치하는 회원 정보가 없습니다."
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
