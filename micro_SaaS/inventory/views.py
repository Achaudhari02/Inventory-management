from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages 
from .forms import SignUpForm, BusinessForm, ProductForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Business, Product, StockTransaction
from django.db.models import Q, F

# Create your views here.

def signup_view(request):

    if request.user.is_authenticated:
        messages.info(request, "You already have an account")
        redirect('dashboard')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account was successfully created')
            return redirect('dashboard')
            # return HttpResponse("<h1>You have signed in </h1>")

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


@login_required
def business_list_view(request):
    businesses = Business.objects.filter(owner=request.user)
    return render(request, 'inventory/business_list.html',{'businesses':businesses})

@login_required
def business_create_view(request):
    if request.method == 'POST':
        form = BusinessForm(request.POST)

        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            business.save()
            request.session['current_business_id'] = business.id
            messages.success(request, f'Business "{business.name}" created!')
            return redirect('dashboard')
            
    else:
        form = BusinessForm()
    return render(request, 'inventory/business_form.html', {
        'form': form,
        'action': 'Create'
    })
@login_required
def business_switch_view(request, business_id):
    business = get_object_or_404(Business, id=business_id, owner=request.user)
    request.session['current_business_id'] = business.id
    messages.success(request, f'Switched to business: {business.name}')
    return redirect('dashboard')

@login_required
def dashboard_view(request):

    business_id = request.session.get("current_business_id")

    if not business_id:
        businesses = Business.objects.filter(owner=request.user)
        if businesses.exists():
            request.session["current_business_id"] = businesses.first().id
            business_id = businesses.first().id
        else:
            return redirect('business_create')
    
    try:
        current_business = Business.objects.get(
            id=business_id,
            owner=request.user
        )
    except Business.DoesNotExist:
        del request.session['current_business_id']
        return redirect('dashboard')
    
    products = Product.objects.filter(business=current_business)

    low_stock_products = products.filter(
        current_quantity__lte = F('reorder_level')
    ) 

    recent_transactions = StockTransaction.objects.filter(
        product__business = current_business
    ).select_related('product').order_by('-created_at')[:10]

    total_products = products.count()
    low_stock_count = low_stock_products.count()
    total_stock_value = 0
    for each in products:
        total_stock_value += each.current_quantity

    context = {

        'current_business': current_business,
        'low_stock_products': low_stock_products,
        'total_products': total_products, 
        'low_stock_count': low_stock_count,
        'total_stock_value': total_stock_value,
        'recent_transactions': recent_transactions, 
    }

    return render(request, 'inventory/dashboard.html', context)


@login_required

def product_list_view(request):
    business_id = request.session['current_business_id']

    if not business_id:
        messages.warning(request, "Please select or create a business first.")
        redirect('dashboard')

    current_business = get_object_or_404(Business,id=business_id,owner=request.user)

    products = Product.objects.filter(business=current_business)

    search_query = request.GET.get('search_query','')
    category_query = request.GET.get('category_query','')

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(sku__icontains=search_query) |
            Q(supplier_name__icontains=search_query)
        )

    if category_query: 
        products = products.filter(
            category=category_query
        )

    categories = Product.objects.values_list('category',flat=True).distinct()
    context = {
        'current_business': current_business,
        'products':products,
        'search': search_query,
        'categories': categories,
        'category_query': category_query
    }

    return render(request, 'inventory/product_list.html',context)

@login_required
def product_create_view(request):

    business_id = request.session["current_business_id"]
    current_business = get_object_or_404(Business,id=business_id,owner=request.user)

    if request.method == "POST":

        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.business = current_business
            product.save()
            messages.success(request, f'{product.name} added successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()

    context = {
        'form': form,
        'current_business': current_business,
        'action': 'Add'
    }

    return render(request, 'inventory/product_add.html',context)

@login_required
def product_update_view(request,product_id):
    business_id = request.session["current_business_id"]
    
    if not business_id:
        messages.error(request,"Please select a business first")
        return redirect('dashboard')
    
    current_business = get_object_or_404(Business,id=business_id,owner=request.user)

    product = Product.objects.get(id=product_id,business=current_business)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'{product.name} successfully updated!')
            return redirect('dashboard')
    else:
        form = ProductForm(instance=product)
    
    context = {
        'action': 'Update',
        'product': product,
        'current_business': current_business,
        'business_id': business_id,
        'form': form
    }

    return render(request, 'inventory/product_add.html', context) 

@login_required
def product_delete_view(request, product_id):

    business_id = request.session["current_business_id"]

    if not business_id:
        messages.warning(request,"Please create or select a business first")
        return redirect('dashboard')
    
    current_business = get_object_or_404(Business,id=business_id,owner=request.user)

    product = get_object_or_404(Product, id=product_id, business=current_business)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('product_list')
    
    context = {

        'product': product.name,
        'business': current_business
    }
    
    return render(request, 'inventory/product_del_confirm.html', context)

     
