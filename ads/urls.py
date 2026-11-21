from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AdViewSet, CommentViewSet

router = DefaultRouter()
router.register('ads', AdViewSet, basename='ads')
router.register(r'ads/(?P<ad_id>\d+)/comments', CommentViewSet, basename='ad-comments')

urlpatterns = [
    path('', include(router.urls)),
]
