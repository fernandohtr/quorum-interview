from django.urls import path

from congress import views

urlpatterns = [
    path("legislators/votes/", views.ListLegislatorsVoteView.as_view(), name="legislator_vote_result"),
    path("bills/votes/", views.ListBillsVoteView.as_view(), name="bill_vote_result"),
]
