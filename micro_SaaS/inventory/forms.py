from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Business, Product, StockTransaction

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )

    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )

    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )

    class Meta: 
        model = User
        fields = ('first_name', 'last_name','username','email','password1','password2')
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ('name','address')


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name','sku','category','current_quantity','reorder_level','unit','supplier_name')
     
class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = ('product', 'type', 'quantity')
        widgets = {
            'product ': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Quantity'
                })
        } 

    def __init__(self, *args, business=None, **kwargs):
        super(StockTransactionForm, self).__init__(*args, **kwargs)
        if business:
            self.fields['product'].queryset  = Product.objects.filter(business=business)