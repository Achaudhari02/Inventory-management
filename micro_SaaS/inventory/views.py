from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages 
from .forms import SignUpForm 
# Create your views here.

def signup_view(request):

    if request.user.is_authenticated:
        redirect('dashboard')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account was successfully created')
            return redirect('dashboard')
    else: 
        form = SignUpForm()
    return render(request, 'inventory/signup.html', {'form': form})


