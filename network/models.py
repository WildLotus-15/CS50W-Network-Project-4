from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class User(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name="profile")
    followers = models.ManyToManyField(User, related_name="following")
    
    def serialize(self, user):
        return {
            "user_id": self.user.id,
            "user_username": self.user.username,
            "followers": self.followers.count(),
            "following": self.user.following.count(),
            "currently_following": not user.is_anonymous and self in user.following.all(),
            "follow_available": (not user.is_anonymous) and self.user != user
        }
    
class Post(models.Model):
    post = models.TextField()
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    likes = models.ManyToManyField(UserProfile, blank=True, related_name="likes")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.post}"

    def serialize(self, user):
        return {
            "id": self.id,
            "post": self.post,
            "date": self.date.strftime("%b %d %Y, %I:%M %p"),
            "author_username": self.author.user.username,
            "author_id": self.author.user.id,
            "likes": self.likes.count(),
            "liked": not user.is_anonymous and self in UserProfile.objects.get(user=user).likes.all(),
            "editable": self.author.user == user
        }

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_created_profile(sender, instance, **kwargs):
    instance.profile.save()