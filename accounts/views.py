from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from django.forms import inlineformset_factory

# we hav e used this in orderform function
from .models import *
from .filters import OrderFilter
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

# this import wil provide the facilty to check the login authentication
from django.contrib.auth import authenticate, login, logout

# this will prevent the anonymous users from entering our site
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .decorators import unauthenticated_user,allowed_users,admin_only


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
@admin_only
def home(request):
    # taking and storing all the orders form Orders
    orders=Order.objects.all()
    customers=Customer.objects.all()

    total_customers=customers.count()
    total_orders=orders.count()
    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()

    context={'orders':orders,'customers':customers,'total_customers':total_customers,
    'total_orders':total_orders,'delivered':delivered,'pending':pending}

    return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    # taking and storing all the products from Products
    products=Product.objects.all()

    return render(request, 'accounts/products.html',{'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customer=Customer.objects.get(id=pk_test)
    orders=customer.order_set.all()

    total_orders=orders.count()

    # we have used request.GET because we want to send it to this view
    myfilter=OrderFilter(request.GET,queryset=orders)
    # this is just taking evry query from the orders and filtering it 
    orders=myfilter.qs

    context={'customer':customer,'orders':orders,'total_orders':total_orders,'myfilter':myfilter}
    return render(request,'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def orderform(request,pk):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=5)
    customer=Customer.objects.get(id=pk)

    # form = OrderForm(initial={'customer':customer})

    # queryset=Order.objects.none()  -> This is helping us to not any data into the form that exists initialy
    formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)

    if request.method=='POST':
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context={'formset':formset}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):

    order=Order.objects.get(id=pk)
    # we are using instance over here because we want to get the -
    # pre-filled data that is already filled into the form 
    form = OrderForm(instance=order)

    if request.method=='POST':
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context={'form':form}

    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):

    order=Order.objects.get(id=pk)

    if request.method=='POST':
        order.delete()
        return redirect('/')

    context={'item':order}
    return render(request, 'accounts/delete.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Customer'])
def UserPage(request):
    orders=request.user.customer.order_set.all()
    print(orders)
    total_orders=orders.count()
    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()

    context={'orders':orders,'total_orders':total_orders,'delivered':delivered,'pending':pending}
    # context={}
    return render(request,'accounts/user.html',context)


@unauthenticated_user
def loginPage(request):

    # we are using request.user.is_authenticed beacuse we are not willing to given access to the 
    # user from this page.
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user=authenticate(request, username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Username or Password is incorrect ")

    context={}
    return render(request,'accounts/login.html',context)

@unauthenticated_user
def register(request):

    # ******* we have commented the below code beacuse insted of that 
    # we have used decorators **************

    # if request.user.is_authenticated:
    #     return redirect('home')

    # else:

    form=CreateUserForm()

    # this post method is taking the input that are given in form and putting it through
    # UserCreationForm method is it is valid then it is saving it .
    # this is the advantage of the django form method
    if request.method=='POST':
        form =CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()

            username=form.cleaned_data.get('username')
            group=Group.objects.get(name='Customer')
            user.groups.add(group)    
            
            Customer.objects.create(
                user=user,
                )

            # this is used to flash a message of success that is imported
            # from django.contrib
            messages.success(request, "account was created for " + username)
            return redirect('login')

    context={'form':form}
    return render(request,'accounts/register.html',context)

def logOutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Customer'])
def accountSettings(request):

    # This is providing me the details of the user that i am logedin with
    customer=request.user.customer
    form=CustomerForm(instance=customer)

    if request.method=='POST':
        form=CustomerForm(request.POST, request.FILES,instance=customer)
        if form.is_valid():
            form.save()

    context={'form':form}
    return render(request,'accounts/account_settings.html',context)