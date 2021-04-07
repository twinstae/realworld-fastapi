import asyncio
from unittest import TestCase
from fastapi.testclient import TestClient
from requests import Response
from app import app
from app.models.orm import User


def get_article_dict(title, description, body, tags):
    return {
        "title": title,
        "description": description,
        "body": body,
        # "tagList": tags
    }


def get_article_data(title, description, body, tags):
    return {
        "article": get_article_dict(
            title, description, body, tags
        )
    }


ARTICLE_URL = '/api/articles'
TAG_URL = '/api/tags/'
REGISTER_URL = '/api/users'
REGISTER_DATA = {
    'user': {
        'username': "stelo",
        'email': "rabolution@gmail.com",
        'password': "test1234"
    }
}
REGISTER_DATA_2 = {
    'user': {
        'username': "taehee",
        'email': "twinstae@naver.com",
        'password': "t1e2s3t4"
    }
}
ARTICLE_1 = get_article_dict('타이틀', '디스크립션', '바디', ['react', '태그'])
ARTICLE_2 = get_article_dict("제목1", "개요2", "내용3", ['django', '태그4'])


class TestCaseWithAuth(TestCase):
    client = TestClient(app)
    token_header_1 = None
    token_header_2 = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.client.__enter__()

    @classmethod
    def tearDownClass(cls) -> None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(User.all().delete())
        cls.client.__exit__()

    @staticmethod
    def check_item(actual_item, expected_item):
        for field_name in expected_item.keys():
            actual_field = actual_item[field_name]
            expected_field = expected_item[field_name]

            if isinstance(expected_field, list):
                assert set(actual_field) == set(expected_field), f"{actual_field} != {expected_field}"
            else:
                assert actual_field == expected_field, f"{actual_field} != {expected_field}"

    def check_item_body(self, actual_body, expected_body):
        key = list(expected_body.keys())[0]
        self.check_item(actual_body[key], expected_body[key])

    def check_sorted_list_body(self, actual_list, expected_list, key):
        assert len(actual_list) == len(expected_list), f"{actual_list}"
        sorted_actual = sorted(actual_list, key=lambda item: item[key])
        sorted_expected = sorted(expected_list, key=lambda item: item[key])
        for actual_item, expected_item in zip(sorted_actual, sorted_expected):
            self.check_item(actual_item, expected_item)

    @classmethod
    def assert_201_CREATED(cls, response: Response):
        cls.assert_status(response, 201)

    @classmethod
    def assert_200_OK(cls, response: Response):
        cls.assert_status(response, 200)

    @classmethod
    def assert_204_NO_CONENT(cls, response: Response):
        cls.assert_status(response, 204)

    @classmethod
    def assert_400_BAD_REQUEST(cls, response: Response):
        cls.assert_status(response, 400)

    @classmethod
    def assert_403_FORBIDDEN(cls, response: Response):
        cls.assert_status(response, 403)

    @classmethod
    def assert_404_NOT_FOUND(cls, response: Response):
        cls.assert_status(response, 404)

    @staticmethod
    def assert_error_detail(response: Response, expected):
        detail = response.json()['errors']['error'][0]
        assert detail == expected, detail

    @staticmethod
    def assert_status(response: Response, code):
        assert response.status_code == code, response.json()

    @classmethod
    def create_users_1_2(cls):
        cls.token_header_1 = cls.register_user(REGISTER_DATA)
        cls.token_header_2 = cls.register_user(REGISTER_DATA_2)

    @classmethod
    def register_user(cls, data):
        response = cls.client.post(REGISTER_URL, json=data)
        assert response.status_code == 201, response.json()
        return cls.get_auth_header(response.json()["user"]["token"])

    @staticmethod
    def get_auth_header(token: str):
        return {"Authorization": "Token "+token}

    @classmethod
    def create_articles_1_2(cls):
        cls.slug_1 = cls.create_article(ARTICLE_1)
        cls.slug_2 = cls.create_article(ARTICLE_2)

    @classmethod
    def create_article(cls, article_dict, token_header=None):
        response = cls.client.post(
            ARTICLE_URL, json={"article": article_dict},
            headers=(token_header or cls.token_header_1)
        )
        cls.assert_201_CREATED(response)
        RESPONSE_JSON = response.json()
        return RESPONSE_JSON["article"]["slug"]
