import factory
from factory.django import DjangoModelFactory

from congress.factories.bill_factory import BillFactory
from congress.factories.vote_factory import VoteFactory
from congress.factories.vote_result_factory import VoteResultFactory
from congress.models import Legislator


class LegislatorFactory(DjangoModelFactory):
    class Meta:
        model = Legislator
        skip_postgeneration_save = True

    name = factory.Faker("name")
    political_party = factory.Iterator(Legislator.PoliticalPartyType.values)
    state = factory.Iterator(Legislator.StateType.values)
    district = factory.Faker("random_int", min=1, max=53)
    congress_house = factory.Iterator(Legislator.CongressHouse.values)
    slug = factory.LazyAttribute(lambda obj: f'{obj.name.lower().replace(" ", "-")}-{obj.state.lower()}-{obj.district}')

    @factory.post_generation
    def votes(self, create, extracted, **kwargs):
        if not create:
            return
        bill1 = BillFactory(sponsor=self)
        bill2 = BillFactory(sponsor=None)
        vote1 = VoteFactory(bill=bill1)
        vote2 = VoteFactory(bill=bill2)
        VoteResultFactory(legislator=self, vote=vote1, vote_type=1)
        VoteResultFactory(legislator=self, vote=vote2, vote_type=2)
