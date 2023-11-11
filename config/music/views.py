from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Music
from django.db.models import Q
from music.serializers import *
from django.http import FileResponse
from django.http import Http404
from .serializers import MusicSerializer
import jwt
from config.settings import SECRET_KEY
from account.models import User


class MusicList(APIView):
    def get(self, request):
        effect_music=Music.objects.filter(music_type='effect')
        bg_music=Music.objects.filter(music_type='background')

        sort_by = request.query_params.get('sort_by', '-upload_date')  # 기본 정렬은 업로드 날짜
        if sort_by == 'length':
            e_music = effect_music.order_by('length')
            b_music=bg_music.order_by('length')

        elif sort_by == '-length':
            e_music = effect_music.order_by('-length')
            b_music=bg_music.order_by('length')
        
        elif sort_by == 'downloads':
            e_music = effect_music.order_by('downloads')
            b_music=bg_music.order_by('downloads')
        
        elif sort_by == '-downloads':
            e_music = effect_music.order_by('-downloads')
            b_music=bg_music.order_by('-downloads')
        
        else:
            e_music = effect_music.order_by('-upload_date')
            b_music=bg_music.order_by('-upload_date')
        
        e_serializer = MusicSerializer(e_music, many=True)
        b_serializer = MusicSerializer(b_music, many=True)
        data={
            "effect_music":e_serializer.data,
            "bg_music":b_serializer.data
        }
        return Response(data,status=status.HTTP_200_OK)
    
    def post(self, request): # 음악 게시물 업로드
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            try: # 요청 데이터에 유저 정보가 있다면 작성자에 추가
                access = str.replace(str(request.headers["Authorization"]), 'Bearer ', '')
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                serializer.save(author=user)
            except: # 없다면 null
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MusicDetail(APIView): # 음악 게시물 상세 페이지
    def get_object(self, pk):
        try:
            return Music.objects.get(pk=pk)
        except Music.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        music = self.get_object(pk)
        serializer = MusicSerializer(music)
        return Response(serializer.data)

    def put(self, request, pk):
        music = self.get_object(pk)
        serializer = MusicSerializer(music, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        music = self.get_object(pk)
        music.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MusicSearch(APIView):
    def get(self, request):
        music_list = Music.objects.none()  # 이전 검색 결과 초기화
        search_word = request.query_params.get('search_words', '')

        # 검색어를 사용하여 Music 모델에서 필터링
        music_list = Music.objects.filter(
            Q(title__icontains=search_word) |
            Q(description__icontains=search_word) |
            Q(genre__icontains=search_word) |
            Q(instruments__icontains=search_word) |
            Q(mood__icontains=search_word) |
            Q(author__username__icontains=search_word) |
            Q(music_type__icontains=search_word)
        ).distinct()

        # 검색어와 정확히 일치하는지 확인
        exact_match_music = Music.objects.filter(
            Q(title__iexact=search_word) |
            Q(description__iexact=search_word) |
            Q(genre__iexact=search_word) |
            Q(instruments__iexact=search_word) |
            Q(mood__iexact=search_word) |
            Q(author__username__icontains=search_word) |
            Q(music_type__icontains=search_word)
        ).first()

        if exact_match_music:
            # 정확한 일치의 경우 해당 음악의 JSON 데이터를 직렬화하여 반환
            serializer = MusicSerializer(exact_match_music)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # 검색 결과가 없으면 빈 JSON 응답 반환
        return Response({}, status=status.HTTP_404_NOT_FOUND)



def download_music(request, music_id):
    music = get_object_or_404(Music, pk=music_id)
    music.downloads+=1
    music.save()

    mp3_file = music.music_file
    response = FileResponse(mp3_file, as_attachment=True)
    return response


class LikeMusic(APIView):
    def get(self, request, music_pk):
        try:
            music = get_object_or_404(Music, id=music_pk)
            serializer = LikeMusicSerializer(music)
            data={
                "msg":"ok",
                "like_userid":serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        except:
            data={
                "msg":"해당 게시물이 존재하지 않습니다."
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, music_pk):
        post = get_object_or_404(Music, id=music_pk)
        # access = request.COOKIES['access']
        access = str.replace(str(request.headers["Authorization"]), 'Bearer ', '')
        payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
        pk = payload.get('user_id')
        user = get_object_or_404(User, pk=pk)

        if user in post.liker.all():
            post.liker.remove(user.id)
            data={
                "msg":"unlike",
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            post.liker.add(user.id)
            data={
                "msg":"like"
            }
            return Response(data, status=status.HTTP_200_OK)