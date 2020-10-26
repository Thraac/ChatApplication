from django.urls import path, re_path

from .views import ThreadView, InboxView, thread_list_view, search_list_view

app_name = 'chat'
urlpatterns = [
    path("", thread_list_view),
    path("search/", search_list_view),
    re_path(r"^(?P<username>[\w.@+-]+)/", ThreadView.as_view()),
]