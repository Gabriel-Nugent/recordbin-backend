from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate , login
from .models import *
from .serializers import *

import musicbrainzngs

# DJANGO APIVIEWS

class RatingManager(APIView):
    def get(self, request):
        _ , auth = request.META['HTTP_AUTHORIZATION'].split()

        release_id = request.GET.get("release")
        user = Token.objects.get(key=auth).user

        if Album.objects.filter(release_id=release_id).exists():
          album = Album.objects.get(release_id=release_id) 
          if Rating.objects.filter(user=user).filter(album=album).exists():
            rating = Rating.objects.filter(user=user).filter(album=album).first()
            return(Response(RatingSerializer(rating).data))
          else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT) 

    def post(self, request):
        _ , auth = request.META['HTTP_AUTHORIZATION'].split()

        user = Token.objects.get(key=auth).user

        if Album.objects.filter(release_id=request.data["release_id"]).exists():
          album = Album.objects.get(release_id=request.data["release_id"])
          if Rating.objects.filter(user=user).filter(album=album).exists():
              rating = Rating.objects.filter(user=user).filter(album=album).first()
              if (request.data["rating"] != 0):
                rating.rating = request.data["rating"]
                rating.status = True
              else:
                rating.rating = 0
                rating.status = not rating.status
              rating.save()
          else:
              rating = Rating(user=user,album=album)
              if (request.data["rating"] != 0):
                  rating.rating = request.data["rating"]
                  rating.status = True
              else:
                rating.rating = 0
                rating.status = not rating.status
              rating.save()
        else:
          new_album = Album(
                release_id=request.data["release_id"],
                group_id=(request.data["group_id"]),
                album_name=(request.data["album_name"]),
                album_image=(request.data["album_cover"]),
                artist=(request.data["artists"])
          )
          new_album.save()
          if Rating.objects.filter(user=user).filter(album=new_album).exists():
              rating = Rating.objects.filter(user=user).filter(album=new_album).first()
              if (request.data["rating"] != 0):
                rating.rating = request.data["rating"]
                rating.status = True
              else:
                rating.rating = 0
                rating.status = not rating.status
              rating.save()
          else:
              rating = Rating(user=user,album=new_album)
              if (request.data["rating"] != 0):
                  rating.rating = request.data["rating"]
                  rating.status = True
              else:
                rating.rating = 0
                rating.status = not rating.status
              rating.save()

        return(Response(status=status.HTTP_200_OK))

class ListChanger(APIView):
    def get(self, request):
        username = request.GET.get("username")
        list_title = request.GET.get("title")
        user = User.objects.get(username=username)
        list = List.objects.get(user=user,title=list_title)

        return(Response(ListSerializer(list).data))

    def post(self, request):
        _ , auth = request.META['HTTP_AUTHORIZATION'].split()

        user = Token.objects.get(key=auth).user

        if Album.objects.filter(release_id=request.data["release_id"]).exists():
            album = Album.objects.get(release_id=request.data["release_id"])
            list = List.objects.filter(user=user).filter(title=request.data["list_name"]).first()
            list.albums.add(album)
            list.save()
        else:
            new_album = Album(
                release_id=request.data["release_id"],
                group_id=(request.data["group_id"]),
                album_name=(request.data["album_name"]),
                album_image=(request.data["album_cover"]),
                artist=(request.data["artists"])
            )
            new_album.save()

            list = List.objects.filter(user=user).filter(title=request.data["list_name"]).first()
            list.albums.add(new_album)
            list.save()
        return(Response(status=status.HTTP_200_OK))
    
    def delete(self, request):
        _ , auth = request.META['HTTP_AUTHORIZATION'].split()
        print(request.data)
        user = Token.objects.get(key=auth).user
        album = Album.objects.get(release_id=request.data["release_id"])
        list = List.objects.filter(user=user).filter(title=request.data["list_name"]).first()
        list.albums.remove(album)
        return(Response(status=status.HTTP_200_OK))
        

class ListManager(APIView):
    def post(self, request):
        _ , auth = request.META['HTTP_AUTHORIZATION'].split()

        # add new list to user
        user = Token.objects.get(key=auth).user
        new_list = List(
            user=user,
            title=request.data["list-title"],
            description=request.data["list-description"]
        )
        new_list.save()

        # return good status
        return(Response(status=status.HTTP_201_CREATED))
    
    def get(self, request):
        _ , auth = request.META['HTTP_AUTHORIZATION'].split()
        user = Token.objects.get(key=auth).user
        
        user_lists = []
        for item in List.objects.filter(user=user):
            user_lists.append(ListSerializer(item).data)
        
        return Response(user_lists)

class ProfileGetter(APIView):
    def get(self, request):
        username = request.GET.get("username")
        query_type = request.GET.get("query_type")

        if query_type == "all":
            profile_data = [];
            for profile in Profile.objects.filter(username__contains=username):
                profile_data.append(ProfileSerializer(profile).data)
            return Response(profile_data)
        elif query_type == "single":
            data = []
            profile = Profile.objects.get(username=username)
            data.append(ProfileSerializer(profile).data)
            
            user = User.objects.get(username=username)
            user_lists = []
            for item in List.objects.filter(user=user):
                user_lists.append(ListSerializer(item).data)
            
            data.append(user_lists)

            return Response(data)

class ProfileManager(APIView):
    #permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def get(self, request):  # Accept username parameter
        _ , auth = request.META['HTTP_AUTHORIZATION'].split()
        user = Token.objects.get(key=auth).user
        
        data = []
        profile = Profile.objects.get(user=user)
        data.append(ProfileSerializer(profile).data)

        user_lists = []
        for item in List.objects.filter(user=user):
            user_lists.append(ListSerializer(item).data)
        
        data.append(user_lists)

        return Response(data)

    def put(self, request):
        # Update the current user's profile
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # Delete the current user's profile
        profile = Profile.objects.get(user=request.user)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# Handles the creation of a new user
class UserRegistration(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        print("User account creation attempted:")
        print(request.data)
        print()

        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            
            # Check if a user with the provided email already exists
            if User.objects.filter(email=email).exists():
                return Response({'message': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if a user with the provided username already exists
            if User.objects.filter(username=username).exists():
                return Response({'message': 'User with this username already exists'}, status=status.HTTP_400_BAD_REQUEST)

            # If both email and username are unique, proceed with registration
            serializer.save()

            new_user = User.objects.get(username=username)
            new_profile = Profile(user=new_user,username=username)
            new_profile.save();

            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Handles user login
class UserLogin(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        identifier = request.data.get('identifier')
        password = request.data.get('password')
        
        if '@' in identifier:
            user = authenticate(email=identifier, password=password)
        else:
            user = authenticate(username=identifier, password=password)
        if user:
            token, create = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
          return Response({'message': 'Invalid login credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
# Creates a user list
class CreateList(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        title = request.data.get('title')
        profile = request.user.profile
        
        # Check if a list with the provided title already exists for this user
        if List.objects.filter(title=title, profile=profile).exists():
            return Response({'message': 'You already have a list with this title'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new list
        serializer = ListSerializer(data={'title': title, 'profile': profile})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Add album to a list    
class AddAlbumToList(APIView):
    def post(self, request, *args, **kwargs):
        list_id = request.data.get('list_id')
        album_id = request.data.get('album_id')
        
        # Check if both list_id and album_id are provided
        if not list_id or not album_id:
            return Response({'message': 'Both list_id and album_id are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the list exists and belongs to the user
        try:
            list_instance = List.objects.get(pk=list_id, profile=request.user.profile)
        except List.DoesNotExist:
            return Response({'message': 'List does not exist or does not belong to the user'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the album is already in the list
        if AlbumInList.objects.filter(list=list_instance, album=album_id).exists():
            return Response({'message': 'Album is already in the list'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new entry in AlbumInList
        serializer = AlbumInListSerializer(data={'list': list_instance.id, 'album': album_id.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# MUSICBRAINZ API REQUESTS 
# Returns a list of relevant searches by artist name 
def search_artist(request):
    if request.method == 'GET':
        artist_name = request.GET.get('artist_name')
        if artist_name:
            # Call the function to search for the artist
            musicbrainzngs.set_useragent("recordbin", "0.1", contact="calebmalvarez@gmail.com")
            artist_list = musicbrainzngs.search_artists(artist_name)
            # Remove unwanted keys
            artist_data = [{'mb_id': artist['id'], 'name': artist['name']} for artist in artist_list.get('artist-list', [])]

            if artist_data:
                # Return the data as a JSON response
                return JsonResponse(artist_data, safe=False)
            else:
                return JsonResponse({'error': 'An error occurred while fetching artist data.'}, status=500)
        else:
            return JsonResponse({'error': 'Please provide an artist name.'}, status=400)

# Returns a specific artist by id
def get_artist(request):
    if request.method == 'GET':
        artist_id = request.GET.get('artist_id')
        if artist_id:
            # Call the function to search for the artist
            musicbrainzngs.set_useragent("recordbin", "0.1", contact="calebmalvarez@gmail.com")
            artist_data = musicbrainzngs.get_artist_by_id(artist_id)

            if artist_data:
                # Return the data as a JSON response
                return JsonResponse(artist_data, safe=False)
            else:
                return JsonResponse({'error': 'An error occurred while fetching artist data.'}, status=500)
        else:
            return JsonResponse({'error': 'Please provide an artist id.'}, status=400)

# Returns a specific release by id
def get_release(request):
    if request.method == 'GET':
        release_id = request.GET.get('release_id')
        if release_id:
            # Call the function to search for the artist
            musicbrainzngs.set_useragent("recordbin", "0.1", contact="calebmalvarez@gmail.com")
            release_data = musicbrainzngs.get_release_group_by_id(release_id)

            if release_data:
                # Return the data as a JSON response
                return JsonResponse(release_data, safe=False)
            else:
                return JsonResponse({'error': 'An error occurred while fetching release data.'}, status=500)
        else:
            return JsonResponse({'error': 'Please provide a release id.'}, status=400)

# Returns a list of relevant searches by release title
def search_release(request):
    if request.method == 'GET':
        release_title = request.GET.get('release_title')
        if release_title:
            # Call the function to search for a release
            musicbrainzngs.set_useragent("recordbin", "0.1", contact="calebmalvarez@gmail.com")
            release_list = musicbrainzngs.search_release_groups(release_title)
            # Remove unwanted keys
            release_data = [{'mb_id': release['id'], 'title': release['title'], 'type': release['type']} for release in release_list.get('release-group-list', [])]

            if release_data:
                # Return the data as a JSON response
                return JsonResponse(release_data, safe=False)
            else:
                return JsonResponse({'error': 'An error occurred while fetching release data.'}, status=500)
        else:
            return JsonResponse({'error': 'Please provide a release title.'}, status=400)

# Returns all of the releases under a given artist by id
def releases_by_artist(request):
    if request.method == 'GET':
        artist_id = request.GET.get('artist_id')
        if artist_id:
            # Call MBDB
            musicbrainzngs.set_useragent("recordbin", "0.1", contact="calebmalvarez@gmail.com")
            release_list = musicbrainzngs.browse_release_groups(artist_id)
            # Remove unwanted keys
            release_data = [{'mb_id': release['id'], 'title': release['title'], 'type': release['type']} for release in release_list.get('release-group-list', [])]

            if release_data:
                # Return the data as a JSON response
                return JsonResponse(release_data, safe=False)
            else:
                return JsonResponse({'error': 'An error occurred while fetching release data.'}, status=500)
        else:
            return JsonResponse({'error': 'Please provide an artist id.'}, status=400)