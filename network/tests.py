from django.test import TestCase
from django.db import IntegrityError
from django.test import TestCase

from .models import User, UserFollowing

# Create your tests here.
class FollowTests(TestCase):
    def test_no_self_follow(self):
        user = User.objects.create()
        constraint_name = "core_follow_prevent_self_follow"
        with self.assertRaisesMessage(IntegrityError, constraint_name):
            UserFollowing.objects.create(from_user=user, to_user=user)