from django import forms


class AddWebsite(forms.Form):
    url = forms.CharField(max_length=32)
    selector = forms.CharField(max_length=64)


