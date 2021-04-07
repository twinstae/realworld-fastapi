import asyncio

from app.models.orm import Article, User
from tests.test_api.testing_util import get_article_data, TestCaseWithAuth, ARTICLE_URL, ARTICLE_1, ARTICLE_2

RETRIEVE_EXPECTED = {
    "article": {
        'body': '바디',
        'description': '디스크립션',
        'favorited': False,
        'favoritesCount': 0,
        'title': '타이틀',
        'tagList': ['react', '태그']
    }
}
CREATE_DATA = get_article_data("제목", "개요", "내용", ["태그"])
UPDATE_DATA = get_article_data("제목있음", "개요있음", "내용있음", ["태그있음"])


class ArticleDangerousTest(TestCaseWithAuth):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.create_users_1_2()

    def tearDown(self) -> None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(Article.all().delete())

    def test_create_article(self):
        response = self.client.post(
            ARTICLE_URL,
            json=CREATE_DATA,
            headers=self.token_header_1
        )
        self.assert_201_CREATED(response)
        RESPONSE_JSON = response.json()

        self.check_item_body(RESPONSE_JSON, CREATE_DATA.copy())
        return RESPONSE_JSON["article"]["slug"]

    def test_init(self):
        response = self.client.get(ARTICLE_URL)
        self.assert_200_OK(response)
        assert response.json() == {"articles": [], "articles_count": 0}

    def test_update_article_by_slug(self):
        self.slug_1 = self.create_article(ARTICLE_1, token_header=self.token_header_1)
        response = self.client.put(
            ARTICLE_URL+"/"+self.slug_1, json=UPDATE_DATA,
            headers=self.token_header_1
        )
        self.assert_200_OK(response)
        self.check_item_body(response.json(), UPDATE_DATA.copy())

    def test_delete_article_by_slug(self):
        self.slug_1 = self.create_article(ARTICLE_1, token_header=self.token_header_1)
        response = self.client.delete(
            ARTICLE_URL+"/"+self.slug_1, headers=self.token_header_1
        )
        self.assert_204_NO_CONENT(response)


class ArticleTest(TestCaseWithAuth):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(User.all().delete())

        cls.create_users_1_2()
        cls.create_articles_1_2()

    def test_retrieve_article_by_slug(self):
        response = self.client.get(ARTICLE_URL+"/"+self.slug_1)
        self.check_item(response.json()["article"], ARTICLE_1)

    def test_list_articles(self):
        response = self.client.get(ARTICLE_URL)
        articles = response.json()["articles"]
        self.check_sorted_list_body(articles, [ARTICLE_1, ARTICLE_2], key="title")
