from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound
from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):

        search_keyword = self.request.GET.get("keyword", None)

        if search_keyword:
            search_result = self.queryset.filter(
                Q(title__icontains=search_keyword)
                | Q(contents__icontains=search_keyword)
            )
            return search_result

        else:
            return self.queryset

    def get_object(self, pk=None):
        try:
            return self.queryset.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound('Not Found')

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'user': request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        post = self.get_object(pk)
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    # method put patch 전부됨
    def update(self, request, pk=None, *args, **kwargs):
        post = self.get_object(pk)
        serializer = self.serializer_class(
            post,
            data=request.data,
            context={'user': request.user},
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)