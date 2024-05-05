from django.urls import path

from congress import views


urlpatterns = [
    path("legislators/votes/", views.legislator_vote_result, name="legislator_vote_result"),
]
