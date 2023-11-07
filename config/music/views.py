from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import status
from .models import Music
from django.views.generic import FormView
from django.db.models import Q
from music.serializers import MusicSerializer

class MusicList(APIView):
    def get(self, request):
        sort_by = request.query_params.get('sort_by', '-upload_date')  # 기본 정렬은 업로드 날짜
        music = Music.objects.all().order_by(sort_by)
        serializer = MusicSerializer(music, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
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
