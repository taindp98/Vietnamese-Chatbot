from django.urls import path
from .views import ConversationManagement, home


urlpatterns = [
    ## edit the prefix /pred to indicate another API
    path(
        "conversation", ConversationManagement.as_view(), name="conversation_management"
    ),
    path("", home, name="BK Assistant Home"),
]
