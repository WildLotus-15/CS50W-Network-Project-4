import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, UserProfile

def posts(request):
    profile = request.GET.get('profile', None)
    if (profile):
        posts = Post.objects.filter(author=profile).order_by('-date')
    else:
        posts = Post.objects.order_by('-date')
    return JsonResponse([post.serialize(request.user) for post in posts], safe=False)

def create_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("post")
        post = Post(author=request.user.profile, post=content)
        post.save()
        return JsonResponse({"message": "Post created successfully."}, status=201)
    if request.method == "PUT":
        data = json.loads(request.body)
        post_id = int(data.get("post_id"))
        new_content = data.get("new_content")
        post = Post.objects.get(pk=post_id)
        post.post = new_content
        post.save()
        return JsonResponse({"success": True}, status=200)
    # if request method is GET redirecting to defult route
    return index(request)

def index(request):
    return render(request, "network/index.html")

def profile(request, profile_id):
    profile = UserProfile.objects.get(pk=profile_id)
    return JsonResponse(profile.serialize(request.user), status=200, safe=False)

def update_follow(request, profile_id):
    profile = UserProfile.objects.get(pk=profile_id)
    if request.user in profile.followers.all():
        profile.followers.remove(request.user)
        request.user.following.remove(profile)
        newStatus = False
    else:
        profile.followers.add(request.user)
        request.user.following.add(profile)
        newStatus = True
    return JsonResponse({"newFollower": newStatus, "newAmount": profile.followers.count()}, status=200)

def load_followed_profiles(request):
    followed_profiles = request.user.following.all()
    posts = Post.objects.filter(author__in=followed_profiles).all()
    return JsonResponse([post.serialize(request.user) for post in posts], safe=False)

def update_like(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user.profile in post.likes.all():
        post.likes.remove(request.user.profile)
        newStatus = False
    else:
        post.likes.add(request.user.profile)
        newStatus = True
    return JsonResponse({"liked": newStatus, "newAmount": post.likes.count()}, status=200)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
