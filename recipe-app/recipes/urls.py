from django.urls import path, include
from .views import recipes_home, export_recipes_csv, about_page, generate_chart, add_recipe
from .views import RecipesListView, RecipesDetailView
from django.conf.urls.static import static
from django.conf import settings

app_name = "recipes"

urlpatterns = [
    path("", recipes_home, name="recipes_home"),
    path("recipes/add/", add_recipe, name="add_recipe"),
    path("recipes/export/", export_recipes_csv, name="export_csv"),
    path("generate-chart/", generate_chart, name="generate_chart"),
    path("recipes/", RecipesListView.as_view(), name="recipes_list"),
    path("list/<pk>", RecipesDetailView.as_view(), name="detail"),
    path("about/", about_page, name="about"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)