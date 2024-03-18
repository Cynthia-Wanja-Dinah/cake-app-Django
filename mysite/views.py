from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from .models import Product, CartItem, Order, OrderItem


def login_request(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                error_message = "Invalid username or password."
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid form submission."
            return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def logout_request(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def index(request):
    return render(request, 'index.html')


def cart(request):
    return render(request, 'cart.html')


def contact(request):
    return render(request, 'contact.html')


def order(request):
    return render(request, 'order.html')


def bread(request):
    products = Product.objects.filter(type='bread')
    return render(request, "bread.html", {'products': products})


def cake(request):
    products = Product.objects.filter(type='cake')
    return render(request, "cakes.html", {'products': products})


def cupcakes(request):
    products = Product.objects.filter(type='cupcake')
    return render(request, "cupcakes.html", {'products': products})


def swissrolls(request):
    products = Product.objects.filter(type='swissroll')
    return render(request, "swissroll.html", {'products': products})


def donuts(request):
    products = Product.objects.filter(type='donuts')
    return render(request, "donuts.html", {'products': products})


def others(request):
    products = Product.objects.filter(type='others')
    return render(request, "others.html", {'products': products})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if created:
        messages.success(request, "Product added to cart successfully.")
    else:
        messages.info(request, "Product is already in the cart.")

    return redirect('view_cart')


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.subtotal() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items,
                                        'total_price': total_price})


@login_required
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('view_cart')


@login_required
def place_order(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number',  None)
        user = request.user  
        cart_items = CartItem.objects.filter(user=user)

        # Calculate total amount
        total_amount = sum(item.subtotal() for item in cart_items)

        # Create order
        order = Order.objects.create(
            user=user,
            shipping_address=address,
            phone_number=phone_number,
            total_amount=total_amount
        )

        # Move cart items to order items
        for cart_item in cart_items:
            order.order_items.create(
                product=cart_item.product,
                price=cart_item.product.price
            )

        # Empty the cart
        cart_items.delete()
        messages.success(request, 'Order placed successfully.')
        return redirect('orders')
    return redirect('index')


@login_required
def order_summary(request):
    user_orders = Order.objects.filter(user=request.user)

    # Initialize a list to store order summaries
    order_summaries = []

    # Iterate over user's orders
    for order in user_orders:
        # Retrieve order items associated with the order
        order_items = OrderItem.objects.filter(order=order)
        total_price = sum(item.price for item in order_items)
        order_summaries.append({'order': order, 'order_items': order_items, 'total_price': total_price})

    return render(request, 'orders.html', {'order_summaries': order_summaries})
