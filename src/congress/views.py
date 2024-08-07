from itertools import zip_longest

from django.views.generic import DetailView, ListView

from congress.filters import BillFilter, LegislatorFilter
from congress.forms import BillVoteResultForm, LegislatorVoteResultForm
from congress.models import Bill, Legislator, Vote, VoteResult


class ListLegislatorsVoteView(ListView):
    template_name = "congress/legislator_vote_result.html"
    context_object_name = "legislators"

    def get_queryset(self):
        legislator_name = self.request.GET.get("name")

        legislators_with_votes = Legislator.objects.legislators_with_votes()

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

        bills_with_counts = Bill.objects.bill_with_counts()

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
        return self.filterset.qs.order_by("name")

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
        legislator_id = context["legislator"].id

        supported_bills = Vote.objects.supported(legislator_id)
        opposed_bills = Vote.objects.opposed(legislator_id)

        votes = zip_longest(supported_bills, opposed_bills, fillvalue="")

        context["votes"] = votes

        return context


class BillList(ListView):
    queryset = Bill.objects.all()
    template = "congress/bill_list.html"
    context_object_name = "bills"

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = BillFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.filterset.form
        return context


class BillDetail(DetailView):
    template_name = "congress/bill_detail.html"
    model = Bill
    context_object_name = "bill"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bill_id = context["bill"].id

        supported_legislators = Legislator.objects.supported(bill_id)
        opposed_legislators = Legislator.objects.opposed(bill_id)

        legislators = zip_longest(supported_legislators, opposed_legislators, fillvalue="")

        context["legislators"] = legislators

        return context
