from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .filters import AdFilter
from .models import Ad, Comment
from .pagination import AdPagination
from .serializers import AdSerializer, CommentSerializer


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.select_related('author').all()
    serializer_class = AdSerializer
    pagination_class = AdPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        queryset = self.filter_queryset(self.get_queryset().filter(author=request.user))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return self.get_serializer(queryset, many=True).data


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_ad(self):
        return get_object_or_404(Ad, pk=self.kwargs.get('ad_id'))

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Comment.objects.none()
        return Comment.objects.select_related('author', 'ad').filter(ad=self.get_ad())

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, ad=self.get_ad())
