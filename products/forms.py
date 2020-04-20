from django import forms

INTEGER_CHOICES= [tuple([x,x]) for x in range(1,10)]
PRICES = [(100,100),(500,500),(1000,1000),(2500,2500),(5000,5000),(10000,10000)]

class CartForm(forms.Form):
    quantity = forms.IntegerField(label="Quantity", widget=forms.Select(choices=INTEGER_CHOICES))

class Filter(forms.Form):
    min_price = forms.IntegerField(label="Min Price:", widget=forms.Select(choices=PRICES))
    max_price = forms.IntegerField(label="Max Price:", widget=forms.Select(choices=PRICES))
