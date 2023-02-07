from django import forms
from data.models import Currency



class SelectCurrency(forms.Form):
    currency = forms.ChoiceField(label='Currency', choices=(), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['currency'].choices = [(c.id, c.name) for c in Currency.objects.all()]



class SetEmail(forms.Form):
    email = forms.CharField(max_length=32)


