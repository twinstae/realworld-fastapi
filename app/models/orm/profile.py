from tortoise import fields
from tortoise.models import Model


class Profile(Model):
    id = fields.IntField(pk=True)
    user = fields.OneToOneField("app.User", related_name="profile")
    username = fields.CharField(16)
    bio = fields.CharField(256, null=True)
    image = fields.CharField(256, null=True)

    followings = fields.ManyToManyField("app.Profile", through="follow", related_name="followers")
    favorite_list = fields.ManyToManyField("app.Article", related_name="favorited", through="favorite")

    async def is_following(self, target):
        if self.id == target.id:
            return False
        return await self.followings.filter(id=target.id).exists()

    async def have_favorited(self, article) -> bool:
        return await self.favorite_list.filter(id=article.id).exists()

    async def favorite(self, article):
        await self.favorite_list.add(article)

    async def unfavorite(self, article):
        await self.favorite_list.remove(article)

    def __str__(self):
        return f"""Profile(id={self.id}, username={self.username})"""
