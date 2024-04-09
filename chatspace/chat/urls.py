from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.messages_page, name='messages_page'),
    path('fetch-messages/', views.fetch_messages, name='fetch_messages'),
    path('send-message/', views.send_message, name='send_message'),
]
