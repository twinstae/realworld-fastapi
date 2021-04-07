import asyncio

from app.models.orm import Article, User
from tests.test_api.testing_util import get_article_data, TestCaseWithAuth, ARTICLE_URL, ARTICLE_1, ARTICLE_2, \
    get_article_dict, USER_2_NAME

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

    def test_create_article_without_token(self):
        response = self.client.post(ARTICLE_URL, json=CREATE_DATA)
        self.assert_403_FORBIDDEN(response)
        assert response.json() == {'errors': ['authentication required']}

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

    def test_update_article_by_slug_without_token(self):
        self.slug_1 = self.create_article(ARTICLE_1, token_header=self.token_header_1)

        response = self.client.put(ARTICLE_URL+"/"+self.slug_1, json=UPDATE_DATA)
        self.assert_403_FORBIDDEN(response)
        assert response.json() == {'errors': ['authentication required']}

    def test_update_article_not_exist(self):
        response = self.client.put(
            ARTICLE_URL + "/존재하지않는슬러그", json=UPDATE_DATA,
            headers=self.token_header_1
        )
        self.assert_404_NOT_FOUND(response)
        assert response.json() == {'errors': ['there is no article for the slug']}

    def test_update_others_article(self):
        self.slug_1 = self.create_article(ARTICLE_1, token_header=self.token_header_1)
        response = self.client.put(
            ARTICLE_URL + "/" + self.slug_1, json=UPDATE_DATA,
            headers=self.token_header_2
        )

        self.assert_400_BAD_REQUEST(response)
        assert response.json() == {'errors': ["You can modify only your article"]}

    def test_delete_article_by_slug(self):
        self.slug_1 = self.create_article(ARTICLE_1, token_header=self.token_header_1)
        response = self.client.delete(
            ARTICLE_URL+"/"+self.slug_1, headers=self.token_header_1
        )
        self.assert_204_NO_CONENT(response)

    def test_delete_article_by_slug_without_token(self):
        self.slug_1 = self.create_article(ARTICLE_1, token_header=self.token_header_1)

        response = self.client.delete(ARTICLE_URL+"/"+self.slug_1)
        self.assert_403_FORBIDDEN(response)
        assert response.json() == {'errors': ['authentication required']}

    def test_delete_article_not_exist(self):
        response = self.client.delete(
            ARTICLE_URL + "/존재하지않는슬러그", headers=self.token_header_1
        )
        self.assert_404_NOT_FOUND(response)
        assert response.json() == {'errors': ['there is no article for the slug']}

    def test_delete_others_article(self):
        self.slug_1 = self.create_article(ARTICLE_1, token_header=self.token_header_1)

        response = self.client.delete(ARTICLE_URL + "/" + self.slug_1, headers=self.token_header_2)
        self.assert_400_BAD_REQUEST(response)
        assert response.json() == {'errors': ["You can delete only your article"]}


class ArticleTest(TestCaseWithAuth):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(User.all().delete())

        cls.create_users_1_2()
        cls.slug_1 = cls.create_article(ARTICLE_1, token_header=cls.token_header_1)
        for i in range(20):
            cls.create_article(get_article_dict(f"아티클{i}", f"디스크립션{i}", f"바디{i}", []), token_header=cls.token_header_1)
        for i in range(20, 40):
            cls.create_article(get_article_dict(f"유저2_아티클{i}", f"디스크립션{i}", f"바디{i}", []), token_header=cls.token_header_2)

    def test_retrieve_article_by_slug(self):
        response = self.client.get(ARTICLE_URL+"/"+self.slug_1)
        self.assert_200_OK(response)
        self.check_item(response.json()["article"], ARTICLE_1)

    def test_retrieve_article_not_exist(self):
        response = self.client.get(ARTICLE_URL+"/존재하지않는슬러그")
        self.assert_404_NOT_FOUND(response)
        assert response.json() == {'errors': ['there is no article for the slug']}

    def test_list_articles(self):
        response = self.client.get(ARTICLE_URL)
        self.assert_200_OK(response)
        self.expect_article_list(response, length=20, first_title=ARTICLE_1["title"], count=41)

    @staticmethod
    def expect_article_list(response, length=20, first_title="타이틀", count=41):
        RESPONSE_JSON = response.json()
        articles = RESPONSE_JSON["articles"]
        assert len(articles) == length
        assert articles[0]["title"] == first_title
        assert RESPONSE_JSON["articles_count"] == count

    def test_list_articles_with_offset(self):
        response = self.client.get(ARTICLE_URL+"?offset=20")
        self.assert_200_OK(response)
        self.expect_article_list(response, length=20, first_title="아티클19", count=41)

    def test_list_articles_with_offset_limit(self):
        response = self.client.get(ARTICLE_URL+"?offset=20&limit=10")
        self.assert_200_OK(response)
        self.expect_article_list(response, length=10, first_title="아티클19", count=41)

    def test_list_articles_by_author(self):
        response = self.client.get(ARTICLE_URL+"?author="+USER_2_NAME)
        self.assert_200_OK(response)
        self.expect_article_list(response, length=20, first_title="유저2_아티클20", count=20)
