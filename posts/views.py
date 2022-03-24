from django.db.models import Q
from rest_framework import status, viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound
from .models import Post
from .serializers import PostSerializer


### 조회,생성: generics.ListCreateAPIView
class PostView(generics.ListCreateAPIView):
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
    
    def get(self, request, *args, **kwargs):                # def list도 가능
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    
    def post(self, request, *args, **kwargs):               # def create도 가능
        serializer = self.serializer_class(
            data=request.data,  
            context={'user': request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


### 개별조회,수정,삭제: APIView
class PostDetailView(APIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    
    def get_object(self, pk=None):
        try:
            return self.queryset.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound('Not Found')
    
    def get(self, request, pk=None, *args, **kwargs):
        post = self.get_object(pk)
        serializer = self.serializer_class(post)
        return Response(serializer.data)
        
    def put(self, request, pk=None, *args, **kwargs):
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

    def delete(self, request, pk=None, *args, **kwargs):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

### 조회: generics.ListAPIView
class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    
    # 1.페이지네이션 없을 때
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
    
    # 2.페이지네이션 있을 때
    # url: http://127.0.0.1:8000/api/list?page=2
    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


### 생성: generics.CreateAPIView
class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(
            data=request.data,  
            context={'user': request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      
        
### 생성,조회,개별조회,수정,삭제: viewset
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