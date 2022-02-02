from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('load', views.posts, name="all_posts"),
    path('load/followed', views.load_followed_profiles, name="followed"),
    path('create_post', views.create_post, name="create_post"),
    path('profile/<int:profile_id>', views.profile, name="profile"),
    path('profile/<int:profile_id>/update_follow', views.update_follow, name="update_follow"),
    path('post/<int:post_id>/update_like', views.update_like, name="update_like"),
]