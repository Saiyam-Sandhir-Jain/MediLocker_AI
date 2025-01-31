from django.urls import path
from . import views
from .api import ReportReaderAPI

urlpatterns = [
    path('report_reader', views.analyze, name='reader'),
    path('api/analyze/', ReportReaderAPI.as_view(), name='report_reader_api'),
]
