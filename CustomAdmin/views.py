from django.shortcuts import render
from mysite.models import Order
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from mysite.forms import CustomAdminRegistrationForm, AdminLoginForm


def register_custom_admin(request):
    if request.method == 'POST':
        form = CustomAdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_login') 
    else:
        form = CustomAdminRegistrationForm()
    return render(request, 'register_admin.html', {'form': form})


def custom_admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('order_list')
            else:
                error_message = "Invalid username or password."
                return render(request, 'admin_login.html', {'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid form submission."
            return render(request, 'admin_login.html', {'form': form, 'error_message': error_message})
    else:
        form = AdminLoginForm()
        return render(request, 'admin_login.html', {'form': form})


@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})


@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        return redirect('order_list')  

    return render(request, 'order_list.html', {'order': order})


def admin_logout_request(request):
    logout(request)
    return redirect('admin_login')