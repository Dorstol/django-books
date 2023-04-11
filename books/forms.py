from django import forms


class BookFilterForm(forms.Form):
    author = forms.CharField(max_length=255, required=False)
    genre = forms.CharField(max_length=255, required=False)
    price_min = forms.DecimalField(max_digits=6, decimal_places=2, required=False)
    price_max = forms.DecimalField(max_digits=6, decimal_places=2, required=False)