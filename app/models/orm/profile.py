from tortoise import fields
from tortoise.models import Model


class Profile(Model):
    id = fields.IntField(pk=True)
    user = fields.OneToOneField("app.models.orm.User", related_name="profile")
    username = fields.CharField(16)
    bio = fields.CharField(256, null=True)
    image = fields.CharField(256, null=True)
    followings = fields.ManyToManyField("app.models.orm.Profile", through="follow", related_name="followers")
    followers = fields.ManyToManyField("app.models.orm.Profile")
    articles = fields.ReverseRelation("app.models.orm.Article")

    async def is_following(self, target):
        return await self.followings.filter(id=target.id).exists()
