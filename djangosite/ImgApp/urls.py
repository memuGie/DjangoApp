from django.urls import path
from django.contrib.auth.views import login, logout

from . import views

app_name = "imgapp"

urlpatterns = [
    path('', views.index, name='index'),
    path('details/<int:user_photo_id>/', views.photo_detail, name='detail'),
    path('login', login, name='login'),
    path('logout', logout, {'next_page': 'imgapp:login'}, name='logout'),
]
