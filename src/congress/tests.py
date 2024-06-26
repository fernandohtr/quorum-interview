import pytest

from congress.factories.bill_factory import BillFactory
from congress.factories.legislator_factory import LegislatorFactory
from congress.models import Bill, Legislator, VoteResult


@pytest.fixture
def legislator_mock():
    return LegislatorFactory.create_batch(5)


@pytest.mark.django_db
class TestLegislatorModelTestCase:
    def test_list_legislators(self, legislator_mock):
        number_of_legislators = Legislator.objects.count()
        assert number_of_legislators == 5

    def test_legislislator_supported(self, legislator_mock):
        bill_id = Bill.objects.filter(vote__voteresult__vote_type=1).first().id
        result = Legislator.objects.supported(bill_id).first()
        assert isinstance(result, Legislator) is True
        assert hasattr(result, "name") is True
        assert result.voteresult_set.first().vote_type == VoteResult.VoteType.SUPPORTES.value

    def test_legislislator_opposed(self, legislator_mock):
        bill_id = Bill.objects.filter(vote__voteresult__vote_type=2).first().id
        result = Legislator.objects.opposed(bill_id).first()
        assert isinstance(result, Legislator) is True
        assert hasattr(result, "name") is True
        assert result.voteresult_set.last().vote_type == VoteResult.VoteType.OPPOSES.value

    def test_legislislator_with_votes(self, legislator_mock):
        assert "supported_votes" in Legislator.objects.legislators_with_votes()[0]
        assert "opposed_votes" in Legislator.objects.legislators_with_votes()[4]


@pytest.mark.django_db
class TestBillModelTestCase:
    def test_list_bills(self, legislator_mock):
        number_of_bills = Bill.objects.count()
        assert number_of_bills == 10

    def test_bill_with_counts(self, legislator_mock):
        assert "title" in Bill.objects.bill_with_counts()[0]
        assert "slug" in Bill.objects.bill_with_counts()[1]
        assert "sponsor__name" in Bill.objects.bill_with_counts()[2]
        assert "sponsor__slug" in Bill.objects.bill_with_counts()[3]
        assert "supported_votes" in Bill.objects.bill_with_counts()[4]
        assert "opposed_votes" in Bill.objects.bill_with_counts()[5]
