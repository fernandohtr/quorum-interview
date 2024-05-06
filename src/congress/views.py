from django.db.models import Case, Count, IntegerField, When
from django.views.generic import DetailView, ListView

from congress.forms import BillVoteResultForm, LegislatorVoteResultForm
from congress.filters import LegislatorFilter
from congress.models import Bill, Legislator, Vote, VoteResult


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


class LegislatorList(ListView):
    queryset = Legislator.objects.all()
    template = "congress/legislator_list.html"
    context_object_name = "legislators"

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = LegislatorFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.filterset.form
        return context


class LegislatorDetail(DetailView):
    template_name = "congress/legislator_detail.html"
    model = Legislator
    context_object_name = "legislator"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        supported_bills = Vote.objects.filter(
            voteresult__vote_type=VoteResult.VoteType.SUPPORTES,
            voteresult__legislator__id=context["legislator"].id,
        ).select_related('bill')

        opposed_bills = Vote.objects.filter(
            voteresult__vote_type=VoteResult.VoteType.OPPOSES,
            voteresult__legislator__id=context["legislator"].id,
        ).select_related('bill')

        votes = self.keep_same_length_votes(supported_bills, opposed_bills)

        context["votes"] = votes

        return context

    def keep_same_length_votes(self, list1, list2):
        len1 = list1.count()
        len2 = list2.count()

        list1 = [l.bill.title for l in list1]
        list2 = [l.bill.title for l in list2]

        max_length = max(len1, len2)

        if len1 < max_length:
            list1 += [""] * (max_length - len1)

        elif len2 < max_length:
            list2 += [""] * (max_length - len2)

        return zip(list1, list2)


class BillDetail(DetailView):
    template_name = "congress/bill_detail.html"
    model = Bill
    context_object_name = "bill"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        supported_legislators = Legislator.objects.filter(
            voteresult__vote_type=VoteResult.VoteType.SUPPORTES,
            voteresult__vote__bill__id=context["bill"].id,
        )

        opposed_legislators = Legislator.objects.filter(
            voteresult__vote_type=VoteResult.VoteType.OPPOSES,
            voteresult__vote__bill__id=context["bill"].id,
        )

        legislators = self.keep_same_length_legislators(supported_legislators, opposed_legislators)

        context["legislators"] = legislators

        return context

    def keep_same_length_legislators(self, list1, list2):
        len1 = list1.count()
        len2 = list2.count()

        list1 = [l.name for l in list1]
        list2 = [l.name for l in list2]

        max_length = max(len1, len2)

        if len1 < max_length:
            list1 += [""] * (max_length - len1)

        elif len2 < max_length:
            list2 += [""] * (max_length - len2)

        return zip(list1, list2)
