from django.urls import path

from congress import views

urlpatterns = [
    path("", views.ListLegislatorsAndBillsView.as_view(), name="index"),
    path("legislators/", views.LegislatorList.as_view(), name="legislator_list"),
    path("legislators/votes/", views.ListLegislatorsVoteView.as_view(), name="legislator_vote_result"),
    path("legislators/<slug:slug>/", views.LegislatorDetail.as_view(), name="legislator_detail"),
    path("bills/votes/", views.ListBillsVoteView.as_view(), name="bill_vote_result"),
    path("bills/<slug:slug>/", views.BillDetail.as_view(), name="bill_detail"),
]
