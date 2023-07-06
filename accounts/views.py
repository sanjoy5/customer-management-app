
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import *
from .forms import CustomerForm, OrderForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_user, admin_only
from django.contrib.auth.models import Group
# Create your views here.


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']

            # group = Group.objects.get(name='customer')
            # user.groups.add(group)

            # Customer.objects.create(
            #     user=user,
            #     name=user.username
            # )

            messages.success(request, 'Account was created for ' + username)
            return redirect("login")

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request, 'Username or Password is Incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all().order_by('-id')
    customers = Customer.objects.all().order_by('-id')
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()

    context = {'orders': orders, 'customers': customers,
               'total_customers': total_customers, 'total_orders': total_orders, 'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def userPage(request):
    customer = request.user.customer
    orders = customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    orderout = orders.filter(status="Out for delivery").count()

    context = {'orders': orders, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending, 'orderout': orderout}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def customerAccount(request):

    context = {}
    return render(request, 'customers/customer_account.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def updateAccount(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'customers/update_account.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin', 'staff'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})



@login_required(login_url='login')
@allowed_user(allowed_roles=['admin', 'staff'])
def customersPage(request):
    customers = Customer.objects.all()

    context = {'customers': customers}
    return render(request, 'customers/customers.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin', 'staff'])
def customerDetails(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders,
               'total_orders': total_orders, 'myFilter': myFilter}
    return render(request, 'customers/customer_details.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin', 'staff'])
def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'orders/order_create.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin', 'staff'])
def singleCustomerOrder(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=6)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset}
    return render(request, 'orders/single_customer_order.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin', 'staff'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'orders/order_update.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin', 'staff'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'orders/order_delete.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin', 'staff'])
def createCustomer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'customers/customer_create.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin', 'staff'])
def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'customers/customer_update.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin', 'staff'])
def deleteCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('/')

    context = {'customer': customer}
    return render(request, 'customers/customer_delete.html', context)
