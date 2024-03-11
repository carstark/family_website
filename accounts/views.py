from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from blog.models import Blog, Vote
import smtplib
from email.message import EmailMessage
import random
import string
from datetime import datetime

given_username = "Mr.X"
sent_key = ""
sent_time = datetime.now()


def signup(request):
    if request.method == 'POST':
        # user has info and wants an account now, i.e. post request
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error': 'Username has already been taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'],
                                                email=request.POST['email1'])
                auth.login(request, user=user)
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'error': 'Passwords must match!'})
    else:
        # user wants to enter info, i.e. get request
        return render(request, 'accounts/signup.html')


def login(request):
    if request.method == 'POST':
        # user has info and wants it checked now, i.e. post request
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user=user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Username or password are incorrect!'})
    else:
        # user wants to enter info, i.e. get request
        return render(request, 'accounts/login.html')


def forgotten(request):
    global given_username
    if request.method == 'POST':
        if request.POST['username'] != "":
            try:
                given_username = request.POST['username']
                user = User.objects.get(username=given_username)
                send_key(given_username, user.email, request)
                return render(request, 'accounts/reset.html', {'given_username': given_username})
            except User.DoesNotExist:
                return render(request, 'accounts/forgotten.html', {'error': 'Username does not exist!'})
        else:
            return render(request, 'accounts/forgotten.html', {'error': 'What Username?!'})
    else:
        # user wants to enter info, i.e. get request
        return render(request, 'accounts/forgotten.html')


def send_key(name, email, request):
    global sent_key, sent_time
    try:
        s = smtplib.SMTP_SSL(host=EMAIL_HOST, port=EMAIL_PORT)
        s.ehlo()
        s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    except Exception as e:
        print(f"Internet problem --> {e}")
        return render(request, 'accounts/forgotten.html', {'error': f'{e} -> Internet problem!?'})

    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_HOST_USER
        msg["Subject"] = f"{name}'s One-Time-Key is..."
        msg["Bcc"] = email
        sent_key = ''.join(random.choices(string.digits, k=4))
        msg.set_content(sent_key)
        s.send_message(msg)
    except Exception as e:
        print(f"Sending problem --> {e}")
        return render(request, 'accounts/forgotten.html', {'error': f'{e} -> Sending problem!?'})

    sent_time = datetime.now()
    s.quit()


def reset(request):
    global given_username, sent_key, sent_time
    if request.method == 'POST':
        # user has info and wants an account now, i.e. post request
        if (datetime.now() - sent_time).total_seconds() < 100:
            if request.POST['password1'] == request.POST['password2']:
                if request.POST['key'] == sent_key:
                    user = User.objects.get(username=given_username)
                    user.set_password(request.POST['password1'])
                    user.save()
                    auth.login(request, user=user)
                    return redirect('home')
                else:
                    return render(request, 'accounts/reset.html', {'error': 'Key is wrong!',
                                                                   'given_username': given_username})
            else:
                return render(request, 'accounts/reset.html', {'error': 'Passwords must match!',
                                                               'given_username': given_username})
        else:
            return render(request, 'accounts/forgotten.html', {'error': 'Key timed out!'})
    else:
        # user wants to enter info, i.e. get request
        return render(request, 'accounts/reset.html')


def logout(request):
    if request.method == 'POST':
        # some browsers like Chrome may load get-requests in the background and hence log you out before you know it
        auth.logout(request)
        return redirect('home')


def home(request):
    users = User.objects.all()[1:]
    creators = {}
    for user in users:
        username = user.username
        joined = user.date_joined.date
        last_login = user.last_login.date
        upvotes = Vote.objects.all().filter(author=user).count()
        blogs_created = Blog.objects.all().filter(author=user).count()
        if blogs_created != 0:
            latest_blog = Blog.objects.all().filter(author=user)[blogs_created-1]
            author_icon = latest_blog.author_icon
        else:
            author_icon = None
        creators[username] = {'joined': joined,
                              'last_login': last_login,
                              'upvotes': upvotes,
                              'blogs_created': blogs_created,
                              'author_icon': author_icon,
                              }
    return render(request, 'accounts/home.html', {'creators': creators})