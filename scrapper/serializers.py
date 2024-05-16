from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers
from re import match


class UUIDSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)


class WikipediaURLSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)

    def validate_url(self, url):
        if match(r'^https://..\.wikipedia.org/wiki/.+', url) is None:
            raise serializers.ValidationError("Not a valid Wikipedia Article URL")

        return url


class ArticleSerializer(WikipediaURLSerializer, UUIDSerializer):
    pass


class PageSerializer(serializers.Serializer):
    total = serializers.IntegerField(min_value=0, required=True)
    page_size = serializers.IntegerField(min_value=0, required=True)
    articles = ArticleSerializer(required=True, many=True)


class PaginationSerializer(serializers.Serializer):
    page = serializers.IntegerField(min_value=1, required=True)


class HTMLSerializer(serializers.Serializer):
    html = serializers.CharField()


class HTMLElementSerializer(serializers.Serializer):
    name_string = serializers.CharField(default="", allow_blank=True)
    class_string = serializers.CharField(default="", allow_blank=True)
    id_string = serializers.CharField(default="", allow_blank=True)


class ValidationErrorSerializer(serializers.Serializer):
    errors = serializers.DictField(
        child=serializers.ListField(child=serializers.CharField())
    )
