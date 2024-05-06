from django.db.models import Case, Count, IntegerField, When
from django.views.generic import DetailView, ListView

from congress.forms import BillVoteResultForm, LegislatorVoteResultForm
from congress.models import Bill, Legislator, VoteResult


class ListLegislatorsVoteView(ListView):
    template_name = "congress/legislator_vote_result.html"
    context_object_name = "legislators"

    def get_queryset(self):
        legislator_name = self.request.GET.get("name")

        legislators_with_votes = Legislator.objects.annotate(
            supported_votes=Count(
                Case(
                    When(voteresult__vote_type=VoteResult.VoteType.SUPPORTES, then=1),
                    output_field=IntegerField(),
                )
            ),
            opposed_votes=Count(
                Case(
                    When(voteresult__vote_type=VoteResult.VoteType.OPPOSES, then=1),
                    output_field=IntegerField(),
                )
            ),
        ).values("name", "supported_votes", "opposed_votes", "slug")

        if legislator_name:
            legislators_with_votes = legislators_with_votes.filter(name__icontains=legislator_name)

        return legislators_with_votes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = LegislatorVoteResultForm()

        return context


class ListBillsVoteView(ListView):
    template_name = "congress/bill_vote_result.html"
    context_object_name = "bills"

    def get_queryset(self):
        bill_title = self.request.GET.get("title")

        bills_with_counts = Bill.objects.annotate(
            supported_votes=Count(
                Case(
                    When(vote__voteresult__vote_type=VoteResult.VoteType.SUPPORTES, then=1),
                    output_field=IntegerField(),
                )
            ),
            opposed_votes=Count(
                Case(
                    When(vote__voteresult__vote_type=VoteResult.VoteType.OPPOSES, then=1),
                    output_field=IntegerField(),
                )
            ),
        ).values("title", "slug", "supported_votes", "opposed_votes", "sponsor__name", "sponsor__slug")

        if bill_title:
            bills_with_counts = bills_with_counts.filter(title__icontains=bill_title).values(
                "title", "slug", "supported_votes", "opposed_votes", "sponsor__name", "sponsor__slug"
            )
        return bills_with_counts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = BillVoteResultForm()

        return context


class ListLegislatorsAndBillsView(ListView):
    template_name = "congress/index.html"
    context_object_name = "legislators"

    def get_queryset(self):
        return Legislator.objects.order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bills"] = Bill.objects.order_by("-number")

        return context


class DetailLegislator(DetailView):
    template_name = "congress/legislator_detail.html"
    model = Legislator
    context_object_name = "legislator"


class DetailBill(DetailView):
    template_name = "congress/bill_detail.html"
    model = Bill
    context_object_name = "bill"
