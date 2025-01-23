from django.urls import path
from . import views

urlpatterns = [
    path('report_reader', views.analyze, name='reader'),
]
