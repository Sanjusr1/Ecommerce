from django import forms


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=150, required=True, label='First name')
    last_name = forms.CharField(max_length=150, required=False, label='Last name')
    email = forms.EmailField(required=True, label='Email')
    address = forms.CharField(max_length=250, required=True, label='Shipping address')
    city = forms.CharField(max_length=100, required=True, label='City')
    postal_code = forms.CharField(max_length=20, required=True, label='Postal code')
    country = forms.CharField(max_length=100, required=True, label='Country')
    phone = forms.CharField(max_length=30, required=False, label='Phone (optional)')
    notes = forms.CharField(widget=forms.Textarea, required=False, label='Notes (optional)')
