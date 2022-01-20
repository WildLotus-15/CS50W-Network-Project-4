
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('profile/<int:profile_id>', views.profile, name="profile"),
    path('profile/<int:profile_id>/followers/add', views.add_follower, name="follow"),
    path('profile/<int:profile_id>/followers/remove', views.remove_follower, name="unfollow"),
    path('profile/<int:profile_id>/followings', views.followings, name="followings")
]
