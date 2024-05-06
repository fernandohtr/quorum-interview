import django_filters

from congress.models import Bill, Legislator


class LegislatorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Legislator
        fields = [
            "political_party",
            "state",
            "congress_house",
        ]


class BillFilter(django_filters.FilterSet):
    sponsor__name = django_filters.CharFilter(lookup_expr="icontains")
    title = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Bill
        fields = [
            "number",
            "origin",
        ]
