from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    followers = models.ManyToManyField("self", through="UserFollowing", related_name="following" , symmetrical=False)

class UserFollowing(models.Model):
    from_user = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_relationships", # Preventing from having multiple follow relationships between users
                fields=["from_user", "to_user"],
            ),
            models.CheckConstraint(
                name="prevent_self_follow", # Checking if from_user is not equal to to_user 
                check=~models.Q(from_user=models.F("to_user"))
            ),
        ]
    
    def __str__(self):
        return f"{self.from_user} to {self.to_user}"

class Post(models.Model):
    post = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.post}"