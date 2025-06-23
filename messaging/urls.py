from django.urls import path
from . import views


app_name = 'messages'


urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('send/<int:recipient_id>/', views.send_message, name='send_message'),
    path('conversation/<int:user_id>/', views.message_thread, name='message_thread'),
    path('message/<int:pk>/', views.message_detail, name='message_detail'),
    path('', views.inbox, name='inbox'),
    path('thread/<int:user_id>/', views.message_thread, name='thread'),


]
