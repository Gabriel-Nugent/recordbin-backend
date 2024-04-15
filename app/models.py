from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    username = models.TextField(max_length=20, blank=False)
    bio = models.TextField(max_length=500, blank=True)
    picture = models.ImageField(upload_to='pictures/', blank=True)
    listened_album_ids = models.ManyToManyField('self', symmetrical=False, related_name='saved_by')
    followed_users = models.ManyToManyField(User, symmetrical=False, related_name='following')

    def __str__(self):        return self.user.username

class Album(models.Model): #foreign key points to artist
    release_id = models.CharField(max_length=50, unique = True, help_text="MusicBrainz ID")
    group_id = models.CharField(max_length=50, unique = True, default="")
    
    album_name = models.CharField(max_length=100)
    album_image = models.TextField(default="No Cover")
    artist = models.TextField(max_length=100)
    release_date = models.DateField()

    def __str__(self):        return self.album_name

class Release(models.Model):  #foreign key points to album
    mb_id = models.CharField(max_length=36, unique = True, help_text="MusicBrainz ID")
    title = models.CharField(max_length=100)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='releases')

    def __str__(self):        return self.title 

class List(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(default="")
    albums = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class AlbumInList(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.list.title} - {self.album.album_name}"