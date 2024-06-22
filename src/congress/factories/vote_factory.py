import factory
from factory.django import DjangoModelFactory

from congress.models import Vote


class VoteFactory(DjangoModelFactory):
    class Meta:
        model = Vote

    bill = factory.SubFactory("congress.factories.BillFactory")
