from uuid import UUID

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .services import WikiScrapService
from .serializers import (
    WikipediaURLSerializer,
    ValidationErrorSerializer,
    UUIDSerializer,
    HTMLSerializer,
    ArticleSerializer,
    PageSerializer,
    PaginationSerializer,
    HTMLElementSerializer,
)


class ScrapViewSet(ViewSet):
    scrap_service = WikiScrapService()

    @extend_schema(
        summary="Get stored Wikipedia Articles from index",
        parameters=[PaginationSerializer],
        responses={
            status.HTTP_200_OK: PageSerializer,
            status.HTTP_404_NOT_FOUND: None,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
        },
        auth=False,
    )
    @action(detail=False, methods=["GET"])
    def get_wikipedia_articles(self, request):
        serializer = PaginationSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=ValidationErrorSerializer({"errors": serializer.errors}).data,
            )
        page = self.scrap_service.get_urls_page(serializer.validated_data["page"], api_settings.PAGE_SIZE)
        if page is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            status=status.HTTP_200_OK,
            data=PageSerializer(page).data,
        )

    @extend_schema(
        summary="Post Wikipedia Article URL to index",
        request=WikipediaURLSerializer,
        responses={
            status.HTTP_201_CREATED: ArticleSerializer,
            status.HTTP_400_BAD_REQUEST: ValidationErrorSerializer,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
        },
        auth=False,
    )
    @action(detail=False, methods=["POST"])
    def post_wikipedia_url(self, request):
        serializer = WikipediaURLSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=ValidationErrorSerializer({"errors": serializer.errors}).data,
            )

        try:
            article = self.scrap_service.add_article(serializer.validated_data["url"])
        except ConnectionError as conn_e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=ValidationErrorSerializer({"errors": {"connection": list(conn_e.args)}}).data,
            )

        return Response(
            status=status.HTTP_201_CREATED,
            data=ArticleSerializer(article).data,
        )

    @extend_schema(
        summary="Delete Wikipedia Article URL from index",
        parameters=[UUIDSerializer],
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_404_NOT_FOUND: None,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
        },
        auth=False,
    )
    @action(detail=False, methods=["DELETE"])
    def delete_wikipedia_url(self, request):
        serializer = UUIDSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=ValidationErrorSerializer({"errors": serializer.errors}).data,
            )

        if not self.scrap_service.drop_article(serializer.validated_data["id"]):
            return Response(
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Get Wikipedia Article Title text",
        responses={
            status.HTTP_200_OK: HTMLSerializer,
            status.HTTP_400_BAD_REQUEST: ValidationErrorSerializer,
            status.HTTP_404_NOT_FOUND: None,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
        },
        auth=False,
    )
    @action(detail=False, methods=["GET"])
    def get_article_title(self, request, id: UUID):
        try:
            title = self.scrap_service.get_title(id)
        except KeyError:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
            )
        except ConnectionError as conn_e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=ValidationErrorSerializer({"errors": {"connection": list(conn_e.args)}}).data,
            )

        return Response(
            status=status.HTTP_200_OK,
            data=HTMLSerializer({"html": title}).data,
        )

    @extend_schema(
        summary="Post Wikipedia Article HTML element name, id or/and class to find",
        request=HTMLElementSerializer,
        responses={
            status.HTTP_200_OK: HTMLSerializer,
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: ValidationErrorSerializer,
            status.HTTP_404_NOT_FOUND: None,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
        },
        auth=False,
    )
    @action(detail=False, methods=["POST"])
    def post_article_element(self, request, id: UUID):
        serializer = HTMLElementSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=ValidationErrorSerializer({"errors": serializer.errors}).data,
            )

        try:
            element = self.scrap_service.get_html_element(id, **serializer.validated_data)
        except KeyError:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
            )
        except ConnectionError as conn_e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=ValidationErrorSerializer({"errors": {"connection": list(conn_e.args)}}).data,
            )

        if element is None:
            return Response(
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(
            status=status.HTTP_200_OK,
            data=HTMLSerializer({"html": element}).data,
        )
