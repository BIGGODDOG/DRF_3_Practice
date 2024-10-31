from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Song, Playlist

class APITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.profile_url = "/api/playlists/"
        self.user = User.objects.create_user(username="test", password="test")
        self.client.force_authenticate(user=self.user)
        self.playlist = Playlist.objects.create(name='playlist', description='desc', owner=self.user)
        self.song = Song.objects.create(title='song', artist='artist')

    def test_create_playlist(self):
        response = self.client.post(self.profile_url, {'name': 'test', 'description': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_playlist(self):
        response = self.client.get(f'{self.profile_url}{self.playlist.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_song_to_playlist(self):
        response = self.client.post(f'{self.profile_url}{self.playlist.id}/add_song/', {'song_id': self.song.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_song_from_playlist(self):
        self.playlist.songs.add(self.song)

        response = self.client.delete(f'{self.profile_url}{self.playlist.id}/remove_song/{self.song.id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
