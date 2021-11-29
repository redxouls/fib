from django.urls import path, re_path

from .views import EchoView, FibView, LogView

urlpatterns = [
    re_path(r'^tutorial/?$', EchoView.as_view()),
    re_path(r'^fibonacci/?$', FibView.as_view()),
    re_path(r'^logs/?$', LogView.as_view()),
]
