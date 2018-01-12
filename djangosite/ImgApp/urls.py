from django.urls import path
from django.contrib.auth.views import login, logout

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login', login, name='login'),
    path('logout', logout, {'next_page': 'login'}, name='logout'),
]
