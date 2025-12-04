from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages 
from .forms import SignUpForm 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

def signup_view(request):

    if request.user.is_authenticated:
        messages.info(request, "You already have an account")
        # redirect('dashboard')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account was successfully created')
            # return redirect('dashboard')
            return HttpResponse("<h1>You have signed in </h1>")

    else: 
        form = SignUpForm()
    return render(request, 'inventory/signup.html', {'form': form})

def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')
        # return HttpResponse("<h1> Dashboard </h1>")
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None: 
            login(request, user)
            messages.success(request, f'Welcome, back {user.first_name} or {user.username} !')
            return redirect('dashboard')
        else: 
            messages.error(request, "Invalid Username or Password")
    return render(request, 'inventory/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out!")
    return redirect('login')

