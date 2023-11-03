from django.shortcuts import render
from .models import Member


def home(request):
    members = Member.objects
    return render(request, 'members/home.html', {'members': members})


def impressum(request):
    return render(request, 'members/impressum.html')


def datenschutz(request):
    return render(request, 'members/datenschutz.html')
