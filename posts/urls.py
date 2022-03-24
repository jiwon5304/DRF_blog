
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    PostView,
    PostDetailView,
    PostListView,
    PostCreateView,
    PostViewSet
    )

router = DefaultRouter(trailing_slash=False)
router.register(r'posts', PostViewSet)
    
urlpatterns = [
    path('post', PostView.as_view()),                               # 조회,생성: generics.ListCreateAPIView
    path('post/<int:pk>', PostDetailView.as_view()),                # 개별조회, 수정, 삭제: APIView
    path('list', PostListView.as_view()),                           # 조회: generics.ListAPIView
    path('create', PostCreateView.as_view()),                       # 생성: generics.CreateAPIView
]

urlpatterns += router.urls