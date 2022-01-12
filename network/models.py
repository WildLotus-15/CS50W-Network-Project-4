from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("self", blank=True, related_name="followers")
    bio = models.CharField(max_length=64, default="No Bio")

class Post(models.Model):
    post = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.post}"