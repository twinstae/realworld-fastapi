from tortoise import fields
from tortoise.models import Model


class Profile(Model):
    id = fields.IntField(pk=True)
    user = fields.OneToOneField("app.User", related_name="profile")
    username = fields.CharField(16)
    bio = fields.CharField(256, null=True)
    image = fields.CharField(256, null=True)
    followings = fields.ManyToManyField("app.Profile", through="follow", related_name="followers")

    async def is_following(self, target):
        return await self.followings.filter(id=target.id).exists()

    def __str__(self):
        return f"""Profile(id={self.id}, username={self.username})"""
