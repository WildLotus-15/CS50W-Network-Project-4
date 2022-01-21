
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('profile/<int:profile_id>', views.profile, name="profile"),
    path('profile/<int:profile_id>/change_following', views.change_following, name="change_following"),
    path('profile/<int:profile_id>/followings', views.followings, name="followings")
]
