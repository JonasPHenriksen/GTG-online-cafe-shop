from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Product

def home(request):
    return render(request, 'products/home.html')  

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def order_product(request):
    product_id = request.GET.get('product_id')
    product = None
    if product_id:
        product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('product_list')  
    else:
        form = OrderForm(initial={'product': product}) if product else OrderForm()
    
    return render(request, 'products/order_product.html', {'form': form, 'product': product})
