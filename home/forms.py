from django import forms

class PriceRangeFilterForm(forms.Form):
    min_price = forms.DecimalField(
        label='Minimum Price',
        required=False,
        widget=forms.NumberInput(attrs={'step': 20, 'min': 0})
    )
    max_price = forms.DecimalField(
        label='Maximum Price',
        required=False,
        widget=forms.NumberInput(attrs={'step': 20})
    )
