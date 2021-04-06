from unittest import TestCase

from starlette.testclient import TestClient
from app import app
from app.models.schemas.base import ArticleBase
from app.services.articles import get_slug_for_article

client = TestClient(app)

article_1 = ArticleBase(
    slug=get_slug_for_article("제목"),
    title="제목",
    description="개요",
    body="내용"
)


class TestArticles(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_get_list_articles(self):
        pass
