from rest_framework import serializers
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        depth = 1

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"
        depth = 1

# User serializer for account creation and authentication
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required = True, style = {'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
            user = User.objects.create_user(**validated_data) # hashing password
            return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email', 'id']

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['user','title', 'description', 'albums']
        depth = 1
    
class AlbumInListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumInList
        fields = ['list', 'album']