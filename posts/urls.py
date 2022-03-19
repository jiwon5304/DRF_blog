
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'posts', PostViewSet)

urlpatterns = [
]
urlpatterns += router.urls