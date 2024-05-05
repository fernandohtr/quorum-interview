from django import forms


class LegislatorVoteResultForm(forms.Form):
    name = forms.CharField()
