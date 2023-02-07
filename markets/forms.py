from django import forms
from .models import Currency


class AddTicker(forms.Form):
    base_currency = forms.ChoiceField(label='Base currency')
    quote_currency = forms.ChoiceField(label='Quote currency')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        currencies = Currency.objects.all()
        self.fields['base_currency'].choices = [(c.id, c.symbol) for c in currencies]
        self.fields['quote_currency'].choices = [(c.id, c.symbol) for c in currencies]






