from uuid import UUID, uuid4

from django.db import models


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    url = models.URLField()


class Page:
    total: int
    page_size: int
    articles: list[Article]

    def __init__(
        self,
        total: int,
        page_size: int,
        articles: list[Article] | None = None,
    ):
        self.total = total
        self.page_size = page_size
        if articles is None:
            articles = []
        self.articles = articles
