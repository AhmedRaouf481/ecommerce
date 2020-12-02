from django.shortcuts import render, redirect
from django.http import JsonResponse, request
from django.contrib.auth import authenticate , login, logout  
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


import json

from .filters import *
from .decorators import *
from .forms import *
from .models import *
# Create your views here.


@authenticatedUser
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            #asign user to its group
            group = Group.objects.get(name='customer') 
            user.groups.add(group)
            #create customer to same user
            username = form.cleaned_data.get('username') 
            user_email = form.cleaned_data.get('email')
            customer = Customer.objects.create(user = user, name = username, email = user_email)

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')  
          
    context = {'form':form}
    return render(request, 'store/register.html', context)

# def CreateCustomer(request):
#     user
#     form = CreateCustomerForm()

@authenticatedUser
def loginPage(request):

    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password) 
        if user is not None:
            login(request, user)
            # print('valid')
            return redirect('/')  
        else:
            messages.info(request, 'Invalid Username OR Password')
    return render(request, 'store/login.html')

def logoutPage(request):
    logout(request)
    return redirect('home')  

@unauthenticatedUser
def home(request):
    if request.user.is_authenticated:
        products = Product.objects.all()
        customer = request.user.customer
        order= Order.objects.get(customer=customer, compelete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

        myfilter = productFilter(request.GET, queryset = products)
        products = myfilter.qs
      


    else:
        products = Product.objects.all()
        cartItems = 0

    context = {'products': products,
        'cartItems': cartItems,
        }
    return render(request, 'store/store.html', context)

@unauthenticatedUser
def product(request, pk):
    product = Product.objects.get(id=pk)
    customer = request.user.customer
    order= Order.objects.get(customer=customer, compelete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
    context = {'product':product,
        'cartItems': cartItems,}
    return render(request, 'store/product.html',context)

@unauthenticatedUser
def cartDataAPI(request):
    customer = request.user.customer
    order= Order.objects.get(customer=customer, compelete=False)
    data = order.orderitem_set.all()
    dataList = []

    for i in data:
        dataList.append({'id' : i.product.id,
        'itemId' : i.id,
        'name' : i.product.name,
        'price' : i.product.price,
        'descreption' : i.product.descreption,
        'image' : i.product.imgUrl,
        'quantity' : i.quantity
        })
    
    return JsonResponse(dataList, safe=False)

@unauthenticatedUser
def cart(request):
    if not request.user.is_authenticated:
        context = {}
    else:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, compelete=False)
        items = order.orderitem_set.all()
        total = order.get_cart_total
        cartItems = order.get_cart_items
           
        context = {'customer': customer,'items': items,
        'total': total,
        'cartItems': cartItems
        }

    return render(request, 'store/cart.html', context)

@unauthenticatedUser
def updateItem(request):
    
    data = json.loads(request.body)
    print(data)
    productId = data['productId']
    action = data['action']
    qty = data['qty']
    print(productId)
    print(action)
    print(qty)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, compelete=False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
    cartItems = order.get_cart_items

    if qty == 1:
        if action == "add":
            orderItem.quantity += 1
        elif action == "remove":
            orderItem.quantity -= 1
    else:
        orderItem.quantity += qty

    # if qty 

    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('item was added', safe=False)

@unauthenticatedUser
def deleteItem(request):
    data = json.loads(request.body)
    itemId = data['id']
    item = OrderItem.objects.get(id=itemId)
    if request.method == 'POST':
        item.delete()
    return JsonResponse('item is deleted', safe=False)

@unauthenticatedUser
def editqty(request):
    data = json.loads(request.body)
    Id = data['id']
    value = data['value']
    print(value)
    item = OrderItem.objects.get(id=Id)
    if request.method == 'POST':
        item.quantity = value
        item.save()
    return JsonResponse('item is deleted', safe=False)

@unauthenticatedUser
def createProduct(request):
    form = CreateProductForm()

    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid')
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'store/form.html', context)

@unauthenticatedUser
def editProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = CreateProductForm(instance=product)

    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            print('valid')
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'store/form.html', context)

@unauthenticatedUser
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('/')

    context = {'item':product}
    return render(request, 'store/delete.html', context)






def aboutus(request):
    return render(request, 'store/about_us.html')

def profile(request):
    return render(request, 'store/profile.html')







