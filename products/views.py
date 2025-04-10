from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from .forms import OrderForm
from .models import Product, BasketItem

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

def add_to_basket(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))  # Get quantity from form or default to 1

    # Use a session to store basket items for unauthenticated users
    basket = request.session.get('basket', {})

    # If the product is already in the basket, update the quantity
    if str(product_id) in basket:
        basket[str(product_id)] += quantity
    else:
        basket[str(product_id)] = quantity

    # Save the updated basket back to the session
    request.session['basket'] = basket

    # Return a JSON response with the updated basket
    return JsonResponse({
        'success': True,
        'message': f'Added {quantity} of {product.name} to the basket.',
        'basket': basket  # Optionally return the updated basket
    })
def view_basket(request):
    basket = request.session.get('basket', {})
    basket_items = []

    # Retrieve product details for each item in the basket
    for product_id, quantity in basket.items():
        product = get_object_or_404(Product, id=product_id)
        basket_items.append({'product': product, 'quantity': quantity})

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user  # Assuming you want to associate the order with the user
            order.save()
            # Clear the basket after placing the order
            request.session['basket'] = {}
            return render(request, 'products/order_confirmation.html', {'order': order})
    else:
        form = OrderForm()

    return render(request, 'products/basket.html', {'basket_items': basket_items, 'form': form})


def place_order(request):
    if request.user.is_authenticated:
        basket_items = BasketItem.objects.filter(user=request.user)
        # Here you would typically create an Order model and save the order details

        # Clear the basket after placing the order
        basket_items.delete()
        return render(request, 'products/order_confirmation.html')
    else:
        return redirect('login')  # Redirect to login if not authenticated