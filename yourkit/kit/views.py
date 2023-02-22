# from django.shortcuts import render
# from django.http import HttpResponseRedirect
from django.http import JsonResponse
# from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import View
from . models import Product, Cart, OrderPlaced, Customer
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q




# Create your views here.
def home(request):
    totalitem = 0
    if request.user.is_authenticated :
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'kit/home.html', locals())

def about(request):
    totalitem = 0
    if request.user.is_authenticated :
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'kit/about.html', locals())
def contact(request):
    totalitem = 0
    if request.user.is_authenticated :
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'kit/contact.html', locals())


class CategoryView(View):
    def get(self,request,val):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "kit/category.html", locals())

class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, "kit/category.html", locals())

class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'kit/productdetail.html', locals())

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'kit/customerresgistration.html', locals())

    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Register Successfully")

        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'kit/customerresgistration.html', locals())

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'kit/profile.html', locals())
    def post(self,request):
   
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
                    
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            area = form.cleaned_data['area']
            zipcode = form.cleaned_data['zipcode']
                    

            reg =Customer(user=user, name=name, locality=locality, city=city, mobile=mobile, area=area, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratualation's! Profile Save Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'kit/profile.html')

def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'kit/address.html', locals())

class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'kit/updateaddress.html', locals())

    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
                    
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.area = form.cleaned_data['area']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratualation's! Profile Updated Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect('address')

def add_to_cart(request):
    if request.user.is_authenticated:

        user = request.user
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
    else:
        return redirect("/accounts/login")
    
    return redirect("/cart")


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 00
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    else:
        return redirect("/accounts/login")
    return render(request, 'kit/addtocart.html', locals())

class checkout(View):
    def get(self,request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items= Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 00
        p=Payment(
            user=user,
            amount=totalamount,

        )
        p.save()
        return render(request, 'kit/checkout.html', locals())

def cod_payment(request):
    if request.method == 'POST':
        # order_id = request.POST.get('order_id')
        # amount = request.POST.get('amount')
        # cust_id = request.POST.get('cust_id')

        user=request.user
        # customer=Customer.objects.get(id=cust_id)

        cart=Cart.objects.filter(user=user)
        for c in cart:
            OrderPlaced(user=user, product=c.product,  quantity=c.quantity).save()
            c.delete()

        messages.success(request, 'Order placed successfully completed')
        return redirect('orders')
    else:
        return redirect('home')

def orders(request):
    order_placed=OrderPlaced.objects.filter(user=request.user)
    totalitem = 0
    if request.user.is_authenticated :
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'kit/orders.html', locals())

def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 00
       
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount

        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 00
        # print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount

        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 00
        # print(prod_id)
        data={
            
            'amount':amount,
            'totalamount':totalamount

        }
        return JsonResponse(data)

def search(request):
    query = request.GET['search']
    totalitem = 0
    if request.user.is_authenticated :
        totalitem = len(Cart.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request, 'kit/search.html', locals())

def searchresult(request):
    if request.user.is_authenticated :
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'kit/searchresult.html', locals())


