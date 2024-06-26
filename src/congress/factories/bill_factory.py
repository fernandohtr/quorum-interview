import factory
from factory.django import DjangoModelFactory

from congress.models import Bill


class BillFactory(DjangoModelFactory):
    class Meta:
        model = Bill

    number = factory.Faker("bothify", text="H.R.####")
    title = factory.Faker("sentence", nb_words=4)
    origin = factory.Iterator(Bill.OriginType.values)
    sponsor = factory.SubFactory("congress.factories.legislator_factory.LegislatorFactory")
    slug = factory.LazyAttribute(lambda obj: f"{obj.number}")
