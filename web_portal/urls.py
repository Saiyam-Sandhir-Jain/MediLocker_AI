from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('research/', views.research, name='research'),
    path('about_us/', views.about_us, name='about_us'),
    path('pricing/', views.pricing, name='pricing'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('about_services/', views.learn_more_about_services, name='about_services'),
]