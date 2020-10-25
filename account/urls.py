from django.urls import path, re_path

from .views import RegisterView

app_name = 'account'
urlpatterns = [
    path("", RegisterView),
]