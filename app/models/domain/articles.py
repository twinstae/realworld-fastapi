from app.models.common import DateTimeModelMixin, IDModelMixin


class Article(IDModelMixin, DateTimeModelMixin):
    slug: str
    title: str
    description: str
    body: str
