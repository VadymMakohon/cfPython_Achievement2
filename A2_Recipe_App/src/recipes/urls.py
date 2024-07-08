from django.urls import path
from .views import recipes_home

app_name = "recipes"

urlpatterns = [
    path("", recipes_home, name="recipes_home"),
]