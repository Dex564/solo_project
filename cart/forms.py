from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=200, initial=1,
                    widget = forms.NumberInput(attrs={'class': 'form-control'}))
    override = forms.BooleanField(required=False, initial=False, 
                        widget=forms.HiddenInput)