from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from .forms import OrderForm
from .models import Product, BasketItem
from django.views.decorators.http import require_POST

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

@require_POST
def add_to_basket(request, product_id):
    quantity = int(request.POST.get('quantity', 1))
    product = get_object_or_404(Product, id=product_id)

    # Initialize the basket in the session if it doesn't exist
    if 'basket' not in request.session:
        request.session['basket'] = {}

    # Update the quantity of the product in the basket
    if str(product.id) in request.session['basket']:
        request.session['basket'][str(product.id)] += quantity
    else:
        request.session['basket'][str(product.id)] = quantity

    # Save the session
    request.session.modified = True

    return JsonResponse({'success': True, 'message': 'Product added to basket!', 'quantity': request.session['basket'][str(product.id)]})

def view_basket(request):
    basket = request.session.get('basket', {})
    basket_items = []
    total_amount = 0.0  # Initialize total amount as a float

    # Retrieve product details for each item in the basket
    for product_id, quantity in basket.items():
        product = get_object_or_404(Product, id=product_id)
        basket_items.append({'product': product, 'quantity': quantity})
        
        # Convert product price to float and calculate total amount
        total_amount += float(product.price) * quantity  # Convert to float

    return render(request, 'products/basket.html', {
        'basket_items': basket_items,
        'total_amount': total_amount,
    })

def place_order(request):
    if request.user.is_authenticated:
        basket_items = BasketItem.objects.filter(user=request.user)
        # Here you would typically create an Order model and save the order details

        # Clear the basket after placing the order
        basket_items.delete()
        return render(request, 'products/order_confirmation.html')
    else:
        return redirect('login')  # Redirect to login if not authenticated