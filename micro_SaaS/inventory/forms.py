from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attr={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )

    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attr={
            'class': 'form-control',
            'placeholder': 'First Name0'
        })
    )

    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attr={
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