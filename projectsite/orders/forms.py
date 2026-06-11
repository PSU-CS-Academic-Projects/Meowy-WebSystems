from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'email', 'phone', 'address', 'city', 'postal_code', 'payment_method']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your full shipping address'}),
            'customer_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Postal Code'}),
        }
