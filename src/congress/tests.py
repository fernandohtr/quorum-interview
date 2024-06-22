import pytest

from congress.factories.legislator_factory import LegislatorFactory
from congress.models import Legislator


@pytest.fixture
def legislator_mock():
    return LegislatorFactory.create_batch(5)


@pytest.mark.django_db
class TestLegislatorModelTestCase:
    def test_list_legislators(self, legislator_mock):
        number_of_legislators = Legislator.objects.count()
        assert number_of_legislators == 5

    def test_legislislator_supported(self, legislator_mock):
        bill_id = Legislator.objects.first().bill_set.first().id
        result = Legislator.objects.supported(bill_id).first()
        assert isinstance(result, Legislator) is True
        assert hasattr(result, "name") is True

    def test_legislislator_with_votes(self, legislator_mock):
        assert isinstance(Legislator.objects.legislators_with_votes()[0]["supported_votes"], int) is True
        assert isinstance(Legislator.objects.legislators_with_votes()[4]["opposed_votes"], int) is True
