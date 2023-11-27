from django.urls import path

from . import views


urlpatterns = [
    path('', views.allblogs, name='allblogs'),
    path('<int:blog_id>/', views.detail, name='detail'),
    path('create', views.create, name='create'),
    path('<int:blog_id>/upvote', views.upvote, name='upvote'),
]


