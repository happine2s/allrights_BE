from .models import User
from .serializers import *
from music.models import Music
from music.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.http import Http404
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import render, get_object_or_404
import jwt
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from config.settings import SECRET_KEY


class signup(APIView):
    def post(self, request):
        serializer=UserSerializer(data=request.data)

        if serializer.is_valid():
            user=serializer.save()

            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "msg": "created",
                    "user_info": serializer.data,
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
            
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            
            return res
        data={
                "msg":"failed"
        }
        return Response(data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class signin(APIView):
    # 로그인
    def post(self, request):
        # 유저 인증
        user = authenticate(
            userid=request.data.get("userid"), password=request.data.get("password")
        )
        # 이미 회원가입 된 유저일 때
        if user is not None:
            serializer = UserSerializer(user)
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {   
                    "message": "login success",
                    "user_info": serializer.data,
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            data={
                "msg":"failed"
            }
            return Response(data,status=status.HTTP_404_NOT_FOUND)


class signout(APIView):
    def delete(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        response = Response({
            "msg": "logout ok"
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response


class auth(APIView):
    # 유저 정보 확인
    def get(self, request):
        try:
            # access token을 decode 해서 유저 id 추출 => 유저 식별
            access = request.COOKIES['access']
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            data = {'refresh': request.COOKIES.get('refresh', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                serializer = UserSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access', access)
                res.set_cookie('refresh', refresh)
                return res
            raise jwt.exceptions.InvalidTokenError

        except(jwt.exceptions.InvalidTokenError):
            # 사용 불가능한 토큰일 때
            return Response(status=status.HTTP_400_BAD_REQUEST)


class update_password(APIView):
    def post(self, request,user_pk):
        try:
            access = request.COOKIES['access']
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            if pk==user_pk:
                user = get_object_or_404(User, pk=user_pk)
            else:
                data={
                    "msg":"해당 회원 정보를 수정할 권한이 없습니다. 토큰을 확인해주세요."
                }
                return Response(data,status=status.HTTP_401_UNAUTHORIZED)

            password1=request.data["password1"]
            password2=request.data["password2"]

            if password1==password2:
                user.set_password(password1)
                user.save()
                data={
                    "msg":"ok"
                }
                return Response(data,status=status.HTTP_202_ACCEPTED)
            else:
                data={
                    "msg":"비밀번호가 일치하지 않습니다."
                }
                return Response(data,status=status.HTTP_406_NOT_ACCEPTABLE)
    
        except:
            data={
                    "msg":"올바르지 않은 토큰입니다."
                }
            return Response(data,status=status.HTTP_403_FORBIDDEN)
            

class update_mypage(APIView): # 로그인한 사용자의 정보 수정
    serializer_class = UpdateMypageSerializer

    def put(self, request, user_pk): # 비밀번호는 변경 안됨
        try:
            access = request.COOKIES['access']
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            
            if pk==user_pk:
                user = get_object_or_404(User, pk=pk)
                #login_user_serializer = UserSerializer(instance=user)
                request_serializer = request.data
                serializer = self.serializer_class(
                    user, data=request_serializer, partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                data={
                    "msg":"해당 회원 정보를 수정할 권한이 없습니다. 토큰을 확인해주세요."
                }
                return Response(data,status=status.HTTP_401_UNAUTHORIZED)
        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            data = {'refresh': request.COOKIES.get('refresh', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')

                user = get_object_or_404(User, pk=pk)
                serializer = UserSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access', access)
                res.set_cookie('refresh', refresh)

                data={
                    "msg":"토큰이 만료되어 갱신되었습니다. 다시 시도해주세요.",
                    "user_info":res
                }
                return Response(data,status=status.HTTP_100_CONTINUE)
            raise jwt.exceptions.InvalidTokenError

        except(jwt.exceptions.InvalidTokenError):
            # 사용 불가능한 토큰일 때
            data={
                "msg":"올바르지 않은 토큰입니다."
            }
            return Response(data,status=status.HTTP_400_BAD_REQUEST)


class mypage(APIView): # url의 user_pk에 대한 마이페이지
    def get_object(self, user_pk):
        try:
            return User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, user_pk):
        try:
            user = self.get_object(user_pk)
            user_serializer = MypageUserSerializer(user)
        except:
            data={
                "msg":"일치하는 회원 정보가 없습니다."
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        else:
            music=Music.objects.filter(author=user_pk)
            music_serializer=MypageMusicSerializer(music, many=True)
            like_music = user.like_music.all()
            like_serializer = MypageMusicSerializer(like_music, many=True)

            data={
                "user_info":user_serializer.data,
                "post": music_serializer.data,
                "save":like_serializer.data
            }

            return Response(data, status=status.HTTP_200_OK)
