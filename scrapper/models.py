from uuid import UUID, uuid4

from django.db import models


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    url = models.URLField()


class Page:
    total: int
    previous_page: str | None
    next_page: str | None
    articles: list[Article]

    def __init__(
        self,
        total: int,
        articles: list[Article] | None = None,
    ):
        self.total = total

        if articles is None:
            articles = []
        self.articles = articles
