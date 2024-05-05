from django.db.models import Count, Case, When, IntegerField
from django.shortcuts import render

from congress.models import Bill, Legislator, VoteResult
from congress.forms import LegislatorVoteResultForm, BillVoteResultForm


def legislator_vote_result(request):
    legislator_name = request.GET.get("name")
    
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
    ).values("id", "name", "supported_votes", "opposed_votes")

    if legislator_name:
        legislators_with_votes = legislators_with_votes.filter(
            name__icontains=legislator_name
        )

    context = {
        "legislators": legislators_with_votes,
        "form": LegislatorVoteResultForm()
    }
    return render(request, "congress/legislator_vote_result.html", context)


def bill_vote_result(request):
    bill_title = request.GET.get("title")

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
        )
    ).values(
        "id", "title", "supported_votes", "opposed_votes", "sponsor__name"
    )

    if bill_title:
        bills_with_counts = bills_with_counts.filter(
            title__icontains=bill_title
        ).values(
            "id", "title", "supported_votes", "opposed_votes", "sponsor__name"
        )

    context = {
        "bills": bills_with_counts,
        "form": BillVoteResultForm(),
    }
    return render(request, "congress/bill_vote_result.html", context)
