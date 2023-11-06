from django.shortcuts import render
from .models import User
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class signup(APIView):
    def post(self, request):
        serializer=SignupSerializer(data=request.data)

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
        