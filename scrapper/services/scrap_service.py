import requests
from bs4 import BeautifulSoup
import re
from uuid import UUID

from scrapper.models import Page, Article


class WikiScrapService:

    @staticmethod
    def get_urls_page(page: int, max_entries: int) -> Page | None:
        out: list[Article] = []
        articles = list(Article.objects.all())

        if page == 1 and not articles:
            return Page(0)

        try:
            for i in range((page-1) * max_entries, page * max_entries):
                out.append(articles[i])
        except IndexError:
            pass

        if not out:
            return None

        return Page(total=len(articles), articles=out)

    @staticmethod
    def add_article(url: str) -> Article:
        response = requests.get(url=url)

        try:
            response.raise_for_status()  # Raise HTTPError if one happened
        except requests.exceptions.HTTPError as e:
            conn_e = ConnectionError()
            conn_e.args = e.args
            raise conn_e

        article = Article(url=url)
        article.save()
        return article

    @staticmethod
    def drop_article(article_id: UUID) -> bool:
        if not Article.objects.filter(id=article_id).exists():
            return False
        Article.objects.filter(id=article_id).delete()
        return True

    @staticmethod
    def _get_bs4(article_id: UUID) -> BeautifulSoup:
        if not Article.objects.filter(id=article_id).exists():
            raise KeyError

        article = Article.objects.get(id=article_id)
        response = requests.get(url=article.url)  # can raise KeyError

        try:
            response.raise_for_status()  # Raise HTTPError if one happened
        except requests.exceptions.HTTPError as e:
            conn_e = ConnectionError()
            conn_e.args = e.args
            raise conn_e

        return BeautifulSoup(response.text, 'html.parser')

    @staticmethod
    def _get_url_prefix(url: str) -> str:
        return url[:url.rfind('/')+1]

    # def get_infobox(self, article_id: UUID) -> str:
    #     soup = self._get_bs4(article_id)
    #     infobox = soup.find('table', class_='infobox vevent')
    #     return (
    #         infobox.prettify(formatter='html')
    #         .replace('\n', '')
    #         .replace('\"', "'")
    #         .replace('/wiki/', self._get_url_prefix(article_id))
    #     )
    @classmethod
    def get_title(cls, article_id: UUID) -> str:
        soup = cls._get_bs4(article_id)
        title = soup.find('span', class_='mw-page-title-main')
        return title.prettify(formatter='html').replace('\n', '').replace('\"', "'")

    @classmethod
    def get_html_element(
            cls,
            article_id: UUID,
            name_string: str = None,
            id_string: str = None,
            class_string: str = None
    ) -> str | None:
        if name_string == "":
            name_string = None
        if id_string == "":
            id_string = None
        if class_string == "":
            class_string = None

        if all(v is None for v in [name_string, id_string, class_string]):
            return None

        soup = cls._get_bs4(article_id)
        element = soup.find(name_string, class_=class_string, id=id_string)
        if element is None:
            return None

        url = Article.objects.get(id=article_id).url

        return (
            element.prettify(formatter='html')
            .replace('\n', '')
            .replace('\"', "'")
            .replace("'/wiki/", cls._get_url_prefix(url))
        )
