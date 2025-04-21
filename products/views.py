from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from .forms import OrderForm
from .models import Product, Order, OrderItem, Category
from django.views.decorators.http import require_POST, require_http_methods
from decimal import Decimal
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def home(request):
    return render(request, 'products/home.html')  

@login_required
def product_list(request):
    category_id = request.GET.get('category', None)
    categories = Category.objects.all()

    if category_id == '':
        category_id = None
        selected_category = None
    else:
        try:
            selected_category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            selected_category = None

    if selected_category:
        products = Product.objects.filter(category=selected_category)
    else:
        products = Product.objects.all()

    drinks = products.filter(category__name='Drinks')
    others = products.exclude(category__name='Drinks')

    return render(request, 'products/product_list.html', {
        'drinks': drinks,
        'others': others,
        'categories': categories,
        'selected_category': selected_category,
    })

@login_required
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

@login_required
@require_POST
def add_to_basket(request, product_id):
    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('size', 'regular') 
    product = get_object_or_404(Product, id=product_id)

    if 'basket' not in request.session:
        request.session['basket'] = {}

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
            'price': str(price_per_item) 
        }

    request.session.modified = True

    return JsonResponse({'success': True, 'message': 'Product added to basket!', 'quantity': request.session['basket'][basket_key]['quantity']})

size_price_map = {
    'small': Decimal('0.5'),
    'medium': Decimal('1.0'),
    'large': Decimal('1.5'),
    'regular': Decimal('0.0'),
}

@login_required
@require_http_methods(['POST'])
def remove_from_basket(request, product_id, size):

    if 'basket' not in request.session:
        request.session['basket'] = {}

    basket_key = f"{product_id}_{size}"
    if basket_key in request.session['basket']:
        del request.session['basket'][basket_key]
        request.session.modified = True
    else:

        basket_key = str(product_id)
        if basket_key in request.session['basket']:
            del request.session['basket'][basket_key]
            request.session.modified = True

    return redirect('view_basket')

@login_required
def view_basket(request):
    basket = request.session.get('basket', {})
    basket_items = []
    total_amount = Decimal('0.0')  

    for basket_key, item_data in basket.items():
        product_id, size = basket_key.split('_')
        product = get_object_or_404(Product, id=product_id)
        quantity = item_data['quantity']
        price_per_item = Decimal(item_data['price'])  

        total_price = price_per_item * quantity
        basket_items.append({'product': product, 'quantity': quantity, 'size': size, 'total_price': total_price})
        total_amount += total_price

    return render(request, 'products/basket.html', {
        'basket_items': basket_items,
        'total_amount': total_amount,
    })

@login_required
def place_order(request):
    if not request.user.is_authenticated:
        return redirect('login')  

    if request.method == 'POST':
        order_name = request.POST.get('order_name')  

        if order_name:
            basket = request.session.get('basket', {})

            if basket:
                order = Order.objects.create(
                    user=request.user.username, 
                    name=order_name,  
                    status='CREATED' 
                )

                for product_id_and_size, item_data in basket.items():
                    product_id, size = product_id_and_size.split('_')
                    product = Product.objects.get(id=int(product_id))
                    quantity = item_data['quantity']
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        size=item_data['size'],  
                        quantity=quantity
                    )

                request.session['basket'] = {}

                return render(request, 'products/order_confirmation.html', {'user_name': request.user.username})

            return redirect('view_basket')

        return redirect('view_basket') 

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def bypass_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, email=email, password=password)

        login(request, user)
        return redirect('home')

    return render(request, 'products/bypass_login.html')
