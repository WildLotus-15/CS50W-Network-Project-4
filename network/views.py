from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import User, Post

from .forms import NewPostForm

def index(request):
    posts = Post.objects.order_by('-date') # Getting most recent posts
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            NewPost = form.save(commit=False)
            NewPost.author = request.user
            NewPost.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/index.html", {
                "form": form,
            })
    return render(request, "network/index.html", {
        "form": NewPostForm,
        "posts": posts
    })

def profile(request, profile_id):
    profile = User.objects.get(pk=profile_id)
    followers = profile.followers.all()
    followings = profile.followings.all()
    number_of_followers = len(followers)
    number_of_followings = len(followings)
    posts = Post.objects.filter(author=profile).order_by('-date')
    number_of_posts = len(posts)
    return render(request, "network/profile.html", {
        "profile": profile,
        "profile_followers": followers,
        "number_of_followers": number_of_followers,
        "profile_followings": followings,
        "number_of_followings": number_of_followings,
        "posts": posts,
        "number_of_posts": number_of_posts,
    })

def add_follower(request, profile_id):
    if request.method == "POST":
        profile = User.objects.get(pk=profile_id)
        request_user = User.objects.get(pk=request.user.id)
        profile.followers.add(request.user)
        request_user.followings.add(profile)
        return HttpResponseRedirect(reverse("profile", args=(profile.id,)))

def remove_follower(request, profile_id):
    if request.method == "POST":
        profile = User.objects.get(pk=profile_id)
        profile.followers.remove(request.user)
        request.user.followings.remove(profile)
        return HttpResponseRedirect(reverse("profile", args=(profile.id,)))

def followings(request, profile_id):
    user = User.objects.get(pk=profile_id)
    followings = user.followings.all()
    posts = Post.objects.filter(author__in=followings).order_by('-date')
    return render(request, "network/followings.html", {
        "posts_of_followings": posts
    })

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
