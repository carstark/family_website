from django.urls import path, include
from . import views


urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('forgotten', views.forgotten, name='forgotten'),
    path('reset', views.reset, name='reset'),
    path('logout', views.logout, name='logout'),
]
