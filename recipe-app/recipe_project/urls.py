from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings #allows access to MEDIA_URL and MEDIA_ROOT
from django.conf.urls.static import static # helper function; create URLs from local folder names
from django.views.generic import TemplateView
from .views import login_view, logout_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("recipes.urls")),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path(
        "success/",
        TemplateView.as_view(template_name="recipes/success.html"),
        name="success",
    ),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)