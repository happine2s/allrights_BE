from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Music
from django.db.models import Q
from music.serializers import *
from django.http import FileResponse
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework import generics
from .serializers import MusicSerializer
from mutagen import File as MutagenFile
from io import BytesIO



class MusicList(APIView):
    def get(self, request):
        sort_by = request.query_params.get('sort_by', '-upload_date')  # 기본 정렬은 업로드 날짜
        if sort_by == 'length':
            music = Music.objects.all().order_by('length')

        elif sort_by == '-length':
            music = Music.objects.all().order_by('-length')
        
        elif sort_by == 'downloads':
            music = Music.objects.all().order_by('downloads')
        
        elif sort_by == '-downloads':
            music = Music.objects.all().order_by('-downloads')
        
        else:
            music = Music.objects.all().order_by('-upload_date')
        
        serializer = MusicSerializer(music, many=True)
        return Response(serializer.data)

class MusicUpload(generics.CreateAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    parser_classes = (FileUploadParser, MultiPartParser)

    def post(self, request):
        music_file = request.data['music_file']

        # Music 모델 생성 및 파일 및 기타 필드 저장
        music = Music()
        music.music_file = music_file
        music.title = request.data['title']
        music.music_type = request.data['music_type']
        music.genre = request.data['genre']
        music.instruments = request.data['instruments']
        music.mood = request.data['mood']
        music.description = request.data['description']
        music.music_image = request.data.get('music_image', None)

        # 파일을 DB에 저장
        music.save()

        # Mutagen을 사용하여 length 계산
        file_extension = music_file.name.split('.')[-1].lower()
        audio = MutagenFile(music_file.temporary_file_path())  # 파일 이름 설정을 위해 temporary_file_path() 사용

        if file_extension in ['.mp3', '.m4a']:
            music.length = audio.info.length
            music.save()

        serializer = MusicSerializer(music)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            try: # 요청 데이터에 유저 정보가 있다면 작성자에 추가
                if self.request.data['author']:
                    serializer.save(author=self.request.user)
            except: # 없다면 null
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MusicDetail(APIView):
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
        search_word = request.query_params.get('search_word', '')

        # 검색어를 사용하여 Music 모델에서 필터링
        music_list = Music.objects.filter(
            Q(title__icontains=search_word) |
            Q(description__icontains=search_word) |
            Q(genre__icontains=search_word) |
            Q(instruments__icontains=search_word) |
            Q(mood__icontains=search_word)
        ).distinct()

        # 시리얼라이저를 사용하여 검색 결과를 JSON으로 변환
        serializer = MusicSerializer(music_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


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
        if request.user in post.liker.all():
            post.liker.remove(request.user)
            data={
                "msg":"unlike",
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            post.liker.add(request.user)
            data={
                "msg":"like"
            }
            return Response(data, status=status.HTTP_200_OK)