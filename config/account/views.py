from django.shortcuts import render
from .models import User
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth
from django.contrib.auth import authenticate


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
        serializer=UserSerializer(data=request.data)

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