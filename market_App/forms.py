from django import forms
from .models import Listings
from .models import ListingComment
from django.contrib.auth.models import User

class Listing_Form(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ['name', 'description', 'price', 'image', 'is_on_campus']

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("confirm_password")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = ListingComment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Write a comment...",
                "class": "w-full p-2 rounded-lg border border-zinc-300 font-figtree"
            })
        }
