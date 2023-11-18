from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth


def signup(request):
    if request.method == 'POST':
        # user has info and wants an account now, i.e. post request
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error': 'Username has already been taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
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


def logout(request):
    if request.method == 'POST':
        # some browsers like Chrome may load get-requests in the background and hence log you out before you know it
        auth.logout(request)
        return redirect('home')
