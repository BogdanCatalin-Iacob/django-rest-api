from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django_rest_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentsDetailSerializer


class CommentList(generics.ListCreateAPIView):
    '''
    List all comments or create a new one if logged in
    '''
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post']

    def perform_create(self, Serializer):
        Serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieve, update, delet a comment by id if you own it
    '''
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentsDetailSerializer
    queryset = Comment.objects.all()
