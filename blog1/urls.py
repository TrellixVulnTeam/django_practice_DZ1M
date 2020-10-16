from django.urls import path
from .views import post_list

app_name = 'blog1'

urlpatterns = [
    path('', post_list, name="post_list")
]
