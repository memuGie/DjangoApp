from django.urls import path
from django.contrib.auth.views import login, logout

from . import views

app_name = "imgapp"

urlpatterns = [
    path('', views.index, name='index'),
    path('login', login, name='login'),
    path('logout', logout, {'next_page': 'imgapp:login'}, name='logout'),
]
