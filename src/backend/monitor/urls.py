from django.urls import path
from .views import *

urlpatterns = [
    ## edit the prefix /pred to indicate another API
    path('conversation', ConversationManagement.as_view(), name = 'conversation_management'),
]