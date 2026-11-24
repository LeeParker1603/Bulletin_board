from rest_framework import serializers

from .models import Ad, Comment


class AdSerializer(serializers.ModelSerializer):
    author_first_name = serializers.ReadOnlyField(source="author.first_name")
    author_last_name = serializers.ReadOnlyField(source="author.last_name")
    author_email = serializers.ReadOnlyField(source="author.email")

    class Meta:
        model = Ad
        fields = (
            "id",
            "title",
            "price",
            "description",
            "author",
            "author_first_name",
            "author_last_name",
            "author_email",
            "created_at",
        )
        read_only_fields = ("id", "author", "created_at")


class CommentSerializer(serializers.ModelSerializer):
    author_first_name = serializers.ReadOnlyField(source="author.first_name")
    author_last_name = serializers.ReadOnlyField(source="author.last_name")
    author_email = serializers.ReadOnlyField(source="author.email")

    class Meta:
        model = Comment
        fields = (
            "id",
            "text",
            "author",
            "author_first_name",
            "author_last_name",
            "author_email",
            "ad",
            "created_at",
        )
        read_only_fields = ("id", "author", "ad", "created_at")
