from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("mailing.urls", "mailings"), namespace="mailings")),
    path("users/", include(("users.urls", "users"), namespace="users")),
]
