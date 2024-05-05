from django import forms


class LegislatorVoteResultForm(forms.Form):
    name = forms.CharField()


class BillVoteResultForm(forms.Form):
    title = forms.CharField()
