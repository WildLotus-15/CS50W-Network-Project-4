
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('post/<int:post_id>', views.change_like, name="change_like"),
    path('post/<int:post_id>/edit', views.edit_post, name="edit_post"),
    path('profile/<int:profile_id>', views.profile, name="profile"),
    path('profile/<int:profile_id>/change_following', views.change_following, name="change_following"),
    path('profile/<int:profile_id>/followings', views.followings, name="followings")
]
