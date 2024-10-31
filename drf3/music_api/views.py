from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Song, Playlist
from .serializers import SongSerializer, PlaylistSerializer
from .permissions import IsOwnerOrReadOnly

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filterset_fields = ['name', 'owner__username']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def songs(self, request, pk=None):
        playlist = self.get_object()
        serializer = SongSerializer(playlist.songs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_song(self, request, pk=None):
        playlist = self.get_object()
        song_id = request.data.get('song_id')
        try:
            song = Song.objects.get(pk=song_id)
            playlist.songs.add(song)
            return Response({'status': 'song added'}, status=status.HTTP_200_OK)
        except Song.DoesNotExist:
            return Response({'status': 'song not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['delete'])
    def remove_song(self, request, pk=None, song_id=None):
        playlist = self.get_object()
        try:
            song = playlist.songs.get(pk=song_id)
            playlist.songs.remove(song)
            return Response({'status': 'song removed'}, status=status.HTTP_200_OK)
        except Song.DoesNotExist:
            return Response({'status': 'song not found'}, status=status.HTTP_404_NOT_FOUND)
