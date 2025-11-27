from django import forms
from .models import Listings

class Listing_Form(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ['name', 'description', 'price']