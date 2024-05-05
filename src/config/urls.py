from django.urls import include, path

urlpatterns = [
    path("congress/", include("congress.urls")),
]
