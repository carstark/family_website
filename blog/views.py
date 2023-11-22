from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Blog


def allblogs(request):
    # blogs is a list of objects
    dtn = datetime.now()
    blogs = Blog.objects.all().filter(pub_date__gt=dtn.replace(year=(dtn.year - 1))).order_by('-pub_date')
    return render(request, 'blog/allblogs.html', {'blogs': blogs})


def detail(request, blog_id):
    detailblog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'blog/detail.html', {'blog': detailblog})


@login_required()
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.FILES['image']:
            blog = Blog()
            if request.POST['pub_date']:
                blog.pub_date = request.POST['pub_date']
            else:
                blog.pub_date = datetime.now().date()
            blog.title = request.POST['title']
            blog.body = request.POST['body']
            if request.POST['url']:
                blog.url = request.POST['url']
            else:
                blog.url = "https://nomenetomen.de"
            blog.image = request.FILES['image']
            blog.author_icon = request.FILES['author_icon']
            blog.author = request.user
            blog.save()
            return redirect('allblogs')
        else:
            return render(request, 'blog/create.html', {'error': 'Alle Felder sind notwendig!'})
    else:
        return render(request, 'blog/create.html')
