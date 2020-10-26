from django.urls import path, re_path

from .views import ThreadView, InboxView, SearchView, thread_list_view

app_name = 'chat'
urlpatterns = [
    path("", thread_list_view),
    re_path(r"^(?P<username>[\w.@+-]+)/", ThreadView.as_view()),
    path("search/", SearchView.as_view())
]