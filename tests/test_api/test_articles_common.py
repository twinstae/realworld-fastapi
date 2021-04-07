from tests.test_api.testing_util import TestCaseWithAuth, ARTICLE_URL, USER_2_NAME


class ArticleTest(TestCaseWithAuth):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.create_users_1_2()
        cls.create_articles_1_2()

    def test_get_article_favorite_without_login(self):
        response = self.client.get(ARTICLE_URL+"/"+self.slug_1)
        self.assert_200_OK(response)
        assert response.json()["article"]["favorite"] is False

    def test_favorite_article(self):
        response = self.favorite(self.slug_1, self.token_header_1)

        self.assert_200_OK(response)
        assert response.json()["article"]["favorite"] is True

        self.unfavorite(self.slug_1, self.token_header_1)  # teardown

    def favorite(self, slug: str, headers):
        return self.client.post(ARTICLE_URL + "/" + slug + "/favorite", headers=headers)

    def unfavorite(self, slug: str, headers):
        return self.client.delete(ARTICLE_URL + "/" + slug + "/favorite", headers=headers)

    def test_unfavorite_article(self):
        self.favorite(self.slug_1, self.token_header_2)

        response = self.unfavorite(self.slug_1, self.token_header_2)

        self.assert_200_OK(response)
        assert response.json()["article"]["favorite"] is False

    def test_get_favorite_article_list(self):
        self.favorite(self.slug_1, self.token_header_2)

        response = self.client.get(ARTICLE_URL+"?favorited="+USER_2_NAME, headers=self.token_header_2)
        self.expect_article_list(response, length=1, first_title="타이틀", count=1)

        self.unfavorite(self.slug_1, self.token_header_2)
