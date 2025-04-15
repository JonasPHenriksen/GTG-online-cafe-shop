from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from .forms import OrderForm
from .models import Product, Order, OrderItem, Category
from django.views.decorators.http import require_POST, require_http_methods
from decimal import Decimal

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
    size = request.POST.get('size', 'regular')  # Default to 'regular' if no size is provided
    product = get_object_or_404(Product, id=product_id)

    # Initialize the basket in the session if it doesn't exist
    if 'basket' not in request.session:
        request.session['basket'] = {}

    # Update the quantity and size of the product in the basket
    basket_key = f"{product.id}_{size}"
    if basket_key in request.session['basket']:
        request.session['basket'][basket_key]['quantity'] += quantity
    else:
        if size == 'regular':
            price_per_item = Decimal(product.price)
        else:
            price_per_item = Decimal(product.price) + Decimal(size_price_map.get(size, '0.0'))

        request.session['basket'][basket_key] = {
            'quantity': quantity,
            'size': size,
            'price': str(price_per_item)  # Convert Decimal to string
        }

    # Save the session
    request.session.modified = True

    return JsonResponse({'success': True, 'message': 'Product added to basket!', 'quantity': request.session['basket'][basket_key]['quantity']})


size_price_map = {
    'small': Decimal('0.5'),
    'medium': Decimal('1.0'),
    'large': Decimal('1.5'),
    'regular': Decimal('0.0'),
}



@require_http_methods(['POST'])
def remove_from_basket(request, product_id, size):
    # Initialize the basket in the session if it doesn't exist
    if 'basket' not in request.session:
        request.session['basket'] = {}

    # Remove the specific size of the product from the basket
    basket_key = f"{product_id}_{size}"
    if basket_key in request.session['basket']:
        del request.session['basket'][basket_key]
        request.session.modified = True
    else:
        # If the size is "regular", try to remove the product without a size
        basket_key = str(product_id)
        if basket_key in request.session['basket']:
            del request.session['basket'][basket_key]
            request.session.modified = True

    return redirect('view_basket')

def view_basket(request):
    basket = request.session.get('basket', {})
    basket_items = []
    total_amount = Decimal('0.0')  # Initialize total amount as a Decimal

    # Retrieve product details for each item in the basket
    for basket_key, item_data in basket.items():
        product_id, size = basket_key.split('_')
        product = get_object_or_404(Product, id=product_id)
        quantity = item_data['quantity']
        price_per_item = Decimal(item_data['price'])  # Convert the price back to Decimal

        total_price = price_per_item * quantity
        basket_items.append({'product': product, 'quantity': quantity, 'size': size, 'total_price': total_price})
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
                for product_id_and_size, item_data in basket.items():
                    product_id, size = product_id_and_size.split('_')
                    product = Product.objects.get(id=int(product_id))
                    quantity = item_data['quantity']
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        size=item_data['size'],  # Use the size from the item_data dictionary
                        quantity=quantity
                    )

                # Clear the basket from the session after placing the order
                request.session['basket'] = {}

                # Redirect to the order confirmation page
                return render(request, 'products/order_confirmation.html', {'user_name': request.user.username})

            # If no name is provided or the basket is empty, redirect to the basket page
            return redirect('view_basket')

        return redirect('view_basket')  # Handle non-POST requests
