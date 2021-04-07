import asyncio

from app.models.orm import User
from app.resources import strings
from tests.test_api.testing_util import TestCaseWithAuth, USER_2_NAME


class ArticleTest(TestCaseWithAuth):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(User.all().delete())
        cls.create_users_1_2()
        cls.create_articles_1_2()

    def test_follow(self):
        response = self.follow(USER_2_NAME, self.token_header_1)

        self.assert_200_OK(response)
        self.check_item_body(response.json(), {"profile": {"following": True}})

        self.unfollow(USER_2_NAME, self.token_header_1)

    def test_follow_존재하지않는_프로필(self):
        response = self.follow("존재하지않는사용자", self.token_header_1)
        self.assert_404_NOT_FOUND(response)
        assert response.json() == {'errors': [strings.USER_DOES_NOT_EXIST_ERROR]}

    def test_unfollow(self):
        self.follow(USER_2_NAME, self.token_header_1)

        response = self.unfollow(USER_2_NAME, self.token_header_1)
        self.assert_200_OK(response)

        self.check_item_body(response.json(), {"profile": {"following": False}})

    def test_unfollow_존재하지않는_프로필(self):
        response = self.unfollow("존재하지않는사용자", self.token_header_1)
        self.assert_404_NOT_FOUND(response)
        assert response.json() == {'errors': [strings.USER_DOES_NOT_EXIST_ERROR]}

    def follow(self, user_name, headers):
        return self.client.post(f"api/profiles/{user_name}/follow", headers=headers)

    def unfollow(self, user_name, headers):
        return self.client.delete(f"api/profiles/{user_name}/follow", headers=headers)

    def test_retrieve_profile_by_username(self):
        response = self.client.get(f"api/profiles/{USER_2_NAME}")
        self.assert_200_OK(response)
        self.check_item_body(response.json(), {"profile": {"following": False}})

    def test_retrieve_profile_로그인한_상태로(self):
        self.follow(USER_2_NAME, self.token_header_1)

        response = self.client.get(f"api/profiles/{USER_2_NAME}", headers=self.token_header_1)
        self.assert_200_OK(response)

        self.check_item_body(response.json(), {"profile": {"following": True}})

    def test_retrieve_존재하지않는_profile(self):
        response = self.client.get(f"api/profiles/존재하지않는사용자", headers=self.token_header_1)
        self.assert_404_NOT_FOUND(response)
        assert response.json() == {'errors': [strings.USER_DOES_NOT_EXIST_ERROR]}
