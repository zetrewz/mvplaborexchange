from django.urls import path

from chat.views import chat_room, holl

app_name = 'chat'

urlpatterns = [
    path('room/<int:application_id>/', chat_room, name='chat_room'),
    path('holl/', holl, name='holl')
]