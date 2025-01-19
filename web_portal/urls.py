from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('research/', views.research, name='research'),
    path('about_us/', views.about_us, name='about_us'),
]