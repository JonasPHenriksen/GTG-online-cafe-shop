from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from .forms import OrderForm
from .models import Product, Order, OrderItem, Category
from django.views.decorators.http import require_POST, require_http_methods

def home(request):
    return render(request, 'products/home.html')  

def product_list(request):
    category_id = request.GET.get('category', None)
    categories = Category.objects.all()

    # If "All" is selected (empty string), treat it as None
    if category_id == '':
        category_id = None
        selected_category = None
    else:
        try:
            selected_category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            selected_category = None

    # Filter products based on the selected category
    if selected_category:
        products = Product.objects.filter(category=selected_category)
    else:
        products = Product.objects.all()

    # Separate products into "Drinks" and "Others"
    drinks = products.filter(category__name='Drinks')
    others = products.exclude(category__name='Drinks')

    return render(request, 'products/product_list.html', {
        'drinks': drinks,
        'others': others,
        'categories': categories,
        'selected_category': selected_category,
    })

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

@require_http_methods(['POST'])
def remove_from_basket(request, product_id):
    # Initialize the basket in the session if it doesn't exist
    if 'basket' not in request.session:
        request.session['basket'] = {}

    # Remove the product from the basket
    if str(product_id) in request.session['basket']:
        del request.session['basket'][str(product_id)]
        request.session.modified = True

    return redirect('view_basket')

def view_basket(request):
    basket = request.session.get('basket', {})
    basket_items = []
    total_amount = 0.0  # Initialize total amount as a float

    # Retrieve product details for each item in the basket
    for product_id, quantity in basket.items():
        product = get_object_or_404(Product, id=product_id)
        total_price = float(product.price) * quantity
        basket_items.append({'product': product, 'quantity': quantity, 'total_price': total_price})
        total_amount += total_price

    return render(request, 'products/basket.html', {
        'basket_items': basket_items,
        'total_amount': total_amount,
    })

def place_order(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect if not logged in

    if request.method == 'POST':
        order_name = request.POST.get('order_name')  # Get the name from the form

        if order_name:
            # Check session for basket items (no need for BasketItem model here)
            basket = request.session.get('basket', {})

            if basket:
                # Create the order with status 'in_progress' and name from the form
                order = Order.objects.create(
                    user=request.user.username,  # Store the username
                    name=order_name,  # Name provided by the user
                    status='in_progress'  # Default status
                )

                # Create OrderItem instances for each item in the session basket
                for product_id, quantity in basket.items():
                    product = Product.objects.get(id=product_id)
                    OrderItem.objects.create(order=order, product=product, quantity=quantity)

                # Clear the basket from the session after placing the order
                request.session['basket'] = {}

                # Redirect to the order confirmation page
                return render(request, 'products/order_confirmation.html', {'user_name': request.user.username})

            # If no name is provided or the basket is empty, redirect to the basket page
            return redirect('view_basket')

        return redirect('view_basket')  # Handle non-POST requests

