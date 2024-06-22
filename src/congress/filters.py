import django_filters

from congress.models import Bill, Legislator


class LegislatorFilter(django_filters.FilterSet):
    class Meta:
        model = Legislator
        fields = {
            "name": ["icontains"],
            "political_party": [],
            "state": [],
            "congress_house": [],
        }


class BillFilter(django_filters.FilterSet):
    sponsor__name = django_filters.ModelChoiceFilter(queryset=Legislator.objects.all())

    class Meta:
        model = Bill
        fields = {
            "number": [],
            "origin": [],
            "title": ["icontains"],
        }
