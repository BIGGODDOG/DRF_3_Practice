from django.db import models
from django.contrib.auth.models import User

class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} by {self.artist}"

class Playlist(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    songs = models.ManyToManyField(Song, related_name="playlists")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")

    def __str__(self):
        return self.name