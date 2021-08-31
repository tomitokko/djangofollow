from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
import requests
from .models import FollowersCount

# Create your views here.

def index(request):
    current_user = request.GET.get('user')
    logged_in_user = request.user.username
    user_followers = len(FollowersCount.objects.filter(user=current_user))
    user_following = len(FollowersCount.objects.filter(follower=current_user))
    user_followers0 = FollowersCount.objects.filter(user=current_user)
    user_followers1 = []
    for i in user_followers0:
        user_followers0 = i.follower
        user_followers1.append(user_followers0)
    if logged_in_user in user_followers1:
        follow_button_value = 'unfollow'
    else:
        follow_button_value = 'follow'

    print(user_followers)
    return render(request, 'index.html', {
        'current_user': current_user,
        'user_followers': user_followers,
        'user_following': user_following,
        'follow_button_value': follow_button_value
    })

def followers_count(request):
    if request.method == 'POST':
        value = request.POST['value']
        user = request.POST['user']
        follower = request.POST['follower']
        if value == 'follow':
            followers_cnt = FollowersCount.objects.create(follower=follower, user=user)
            followers_cnt.save()
        else:
            followers_cnt = FollowersCount.objects.get(follower=follower, user=user)
            followers_cnt.delete()
        
        return redirect('/?user='+user)

def register(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save();
                return redirect('login')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('register')
        return redirect('/')
    else:
        return render(request, 'signup.html')

def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')

    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')