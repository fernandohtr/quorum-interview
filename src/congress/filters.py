import django_filters

from congress.models import Bill, Legislator


class LegislatorFilter(django_filters.FilterSet):
    class Meta:
        model = Legislator
        fields = [
            "name",
            "political_party",
            "state",
            "congress_house",
        ]


class BillFilter(django_filters.FilterSet):
    class Meta:
        model = Bill
        fields = [
            "number",
            "title",
            "origin",
            "sponsor__name",
        ]
