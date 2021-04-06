from tortoise import fields
from tortoise.models import Model


class Article(Model):
    id = fields.IntField(pk=True)
    slug = fields.CharField(128, unique=True)
    title = fields.CharField(64)
    description = fields.CharField(128)
    body = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    author = fields.ForeignKeyField('app.models.orm.Profile', related_name="articles")

    def __repr__(self):
        return f"""Article(
            id={self.id},
            title={self.title[:16]},
            description={self.description[:16]},
            body={self.body[:16]},
        )"""
