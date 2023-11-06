from django.shortcuts import render
from .models import User
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password


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
        