from django.urls import path
from .views import chat, get_bot_response

urlpatterns = [
    path('chatbot/', chat, name='chatbot'),
    path('send/', get_bot_response, name='get_bot_response'),
]
