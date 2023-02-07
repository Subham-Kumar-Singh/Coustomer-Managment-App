from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from django.forms import inlineformset_factory

# we hav e used this in orderform function
from .models import *
from .filters import OrderFilter
from .forms import OrderForm


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

def products(request):
    # taking and storing all the products from Products
    products=Product.objects.all()

    return render(request, 'accounts/products.html',{'products':products})

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


def deleteOrder(request,pk):

    order=Order.objects.get(id=pk)

    if request.method=='POST':
        order.delete()
        return redirect('/')

    context={'item':order}
    return render(request, 'accounts/delete.html',context)