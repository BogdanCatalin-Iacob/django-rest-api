from django.db.models import Count
from rest_framework import generics, filters
from django_rest_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):
    '''
    List all profiles
    No profile creation as it is handled by django signals
    '''
    serializer_class = ProfileSerializer

    # add specific fields to queryset
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')


class ProfileDetail(generics.RetrieveUpdateAPIView):
    '''
    Retrieve or update profile if you are the owner
    '''
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    