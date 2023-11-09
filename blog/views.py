from django.shortcuts import render, get_object_or_404
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
