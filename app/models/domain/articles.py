from app.models.common import DateTimeModelMixin, IDModelMixin


class ArticleBase(IDModelMixin, DateTimeModelMixin):
    slug: str
    title: str
    description: str
    body: str
