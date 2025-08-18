from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("mailings/", include("mailings.urls", namespace="mailings")),
    path("newsletters/", include("newsletters.urls", namespace="newsletters")),
    path("", include(("users.urls", "users"), namespace="users")),
]
