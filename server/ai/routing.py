from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/ai/tony/$', consumers.TonyAIConsumer),
    re_path(r'ws/ai/jessie/$', consumers.JessieAIConsumer),
    re_path(r'ws/ai/max/$', consumers.MaxAIConsumer),
]