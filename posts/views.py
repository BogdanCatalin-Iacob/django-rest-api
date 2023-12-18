from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_rest_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    '''
    List all posts.
    Create a post if logged in.
    perform_create associates the post with logged in user
    '''
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = Post.objects.annotate(
        comments_count = Count('owner__comment', distinct=True),
        likes_count = Count('owner__like', distinct=True)
    ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_fields = [
        'comments_count',
        'likes_count',
        'likes__created_at'
    ]


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieve a post and edit or delete it
    '''
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.annotate(
        comments_count = Count('owner__comment', distinct=True),
        likes_count = Count('owner__like', distinct=True)
    ).order_by('-created_at')
