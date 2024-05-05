from django.urls import path, include

urlpatterns = [
    path("congress/", include("congress.urls")),
]
