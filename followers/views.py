from rest_framework import generics, permissions
from django_rest_api.permissions import IsOwnerOrReadOnly
from followers.models import Follower
from followers.serializers import FollowerSerialzier


class FollowerList(generics.ListCreateAPIView):
    '''
    List all followers.
    Create a follower.
    perform_create method associate the current logged user woth a follower
    '''
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = FollowerSerialzier
    queryset = Follower.objects.all()

    def perform_create(self, serializer):
        serializer.save(ownr=self.request.user)
    

class FollowerDetail(generics.RetrieveDestroyAPIView):
    '''
    Retrieve a follower.
    No Update view, only follow or unfollow someone.
    Destroy a follower happens when unfollow someone
    '''
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerialzier