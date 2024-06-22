import factory
from factory.django import DjangoModelFactory

from congress.models import VoteResult


class VoteResultFactory(DjangoModelFactory):
    class Meta:
        model = VoteResult

    legislator = factory.SubFactory("congress.factories.LegislatorFactory")
    vote = factory.SubFactory("congress.factories.VoteFactory")
    vote_type = factory.Iterator(VoteResult.VoteType.values)
