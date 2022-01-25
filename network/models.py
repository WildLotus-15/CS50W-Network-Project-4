from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follower = models.ManyToManyField("self", blank=True, related_name="followers", symmetrical=False)
    following = models.ManyToManyField("self", blank=True, related_name="followings", symmetrical=False)
    bio = models.CharField(max_length=64, default="No Bio")

class Post(models.Model):
    post = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.post}"    