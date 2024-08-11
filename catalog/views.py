from django.http import HttpResponse
from django.shortcuts import render,redirect
from catalog.models import Category,Product,ShoppingCart, ShoppingOrder, DeliveryAddress
from catalog.forms import ProductForm, SignupForm, LoginForm

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from catalog.serializers import CategorySerializer,CategoryCreateSerializer

# Create your views here.

### apis defined here

class CategoryList(APIView):
    def get(self,request):
        categories = Category.objects.all()
        serializers = CategorySerializer(categories,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    def post(self,request):
        serializer = CategoryCreateSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class CategoryDetail(APIView):
    def get(self,request,id):
        category = Category.objects.get(id=id)
        serializer = CategorySerializer(category)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def put(self,request,id):
        category = Category.objects.get(id=id)
        serializer = CategorySerializer(category,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        category = Category.objects.get(id=id)
        category.delete()
        return Response({'message':"success"},status=status.HTTP_200_OK)

###

def get_dummy(request):
    if request.method =='POST':
        print("hello")
    else:
        print("Thank you")
    return render(request,"test.html")

def home(request):
    products = Product.objects.all()
    return render(request,'index.html',{'products':products})

def user_signup(request):
    if request.method=="POST":
        print(request.POST)
        form= SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form= SignupForm()
    return render(request,'signup.html',{'form':form})

def user_login(request):
    if request.method=='POST':
        form= LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return redirect("/")
    else:
        form= LoginForm()
    return render(request,'login.html',{'form':form})

def user_logout(request):
    logout(request)
    return redirect('/login/')

def create_product(request):
    if request.method=="POST":
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/create/product')
    else:
        form=ProductForm()
    return render(request,'create_product.html',{'form':form})


def list_product(request):
    products = Product.objects.all()
    context_dict = {'products':products}
    return render(request, 'list_product.html',context_dict)


def update_product(request,id):
    product = Product.objects.get(id=id)
    if request.method=="POST":
        form = ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            return redirect('/create/product/')
    else:
        form=ProductForm(instance=product)
    return render(request,'create_product.html',{'form':form})

# for shopping cart

def product_detail(request,id):
    product= Product.objects.get(id=id)
    return render(request,'product_detail.html',{'product':product})

@login_required(login_url="/login/")
def add_to_cart(request,id):
    product = Product.objects.get(id=id)
    quantity = request.POST['quantity']
    user = User.objects.get(id=request.user.id)
    cart = ShoppingCart(product=product,quantity=quantity,user=user)
    cart.save()
    return HttpResponse("Success <a href='/'>Go Back</a>")

@login_required(login_url="/login/")
def cart_detail(request):
    user = User.objects.get(id=request.user.id)
    items = ShoppingCart.objects.filter(user=user)
    return render(request,'cart_detail.html',{'items':items})

@login_required(login_url="/login/")
def cart_item_delete(request,id):
    cart = ShoppingCart.objects.get(id=id)
    cart.delete()
    return redirect('/my/cart/')

@login_required(login_url="/login/")
def cart_item_update(request,id):
    cart = ShoppingCart.objects.get(id=id)
    if request.method=='POST':
        quantity = request.POST['quantity']
        cart.quantity = quantity
        cart.save()
        return redirect('/my/cart/')
    return render(request,'cart_edit.html',{'cart':cart})


@login_required(login_url="/login/")
def order_checkout(request):
    user = User.objects.get(id=request.user.id)
    items = ShoppingCart.objects.filter(user=user)
    total_amount = 0
    for item in items:
        total_amount = total_amount+((item.quantity)*(item.product.price))
    shop_order = ShoppingOrder(user=user,total_amount=total_amount)
    shop_order.save()
    return redirect(f'/payment/{shop_order.id}/')

@login_required(login_url="/login/")
def make_payment(request,id):
    shop_order = ShoppingOrder.objects.get(id=id)
    if request.method=='POST':
        paid_amount = request.POST['paid_amount']
        payment_mode = request.POST['payment_mode']
        shop_order.paid_amount = paid_amount
        shop_order.payment_mode = payment_mode
        shop_order.save() 
        return redirect(f'/delivery/address/{shop_order.id}/')
    return render(request,'payment.html',{'shop_order':shop_order})

@login_required(login_url="/login/")
def order_delivery_address(request,id):
    shop_order = ShoppingOrder.objects.get(id=id)
    user = User.objects.get(id=request.user.id)
    delivery_address = DeliveryAddress.objects.filter(user = user)
    if request.method=='POST':
        delivery_address = DeliveryAddress.objects.create(user=user,address = request.POST['address'])
        shop_order.address = delivery_address
        shop_order.payment_status = '0'
        shop_order.delivery_status = '0'
        shop_order.save()
        return HttpResponse('<h1>Order Placed Successfully</h1>.<a href="/">Home</a>')
    return render(request,'address.html',{'shop_order':shop_order,'delivery_address':delivery_address})

@login_required(login_url="/login/")
def place_order(request,id):
    user = User.objects.get(id=request.user.id)
    delivery_address = DeliveryAddress.objects.filter(user = user)[0]
    shop_order = ShoppingOrder.objects.get(id=id)
    shop_order.address = delivery_address
    shop_order.payment_status = '0'
    shop_order.delivery_status = '0'
    shop_order.save()
    return HttpResponse('<h1>Order Placed Successfully</h1>.<a href="/">Home</a>')

@login_required(login_url="/login/")
def show_dashboard(request):
    if request.user.is_superuser:
        orders = ShoppingOrder.objects.all()
        return render(request,'dashboard.html',{'orders':orders})
    else:
        return redirect("/")







## this is a test from my pc using my laptop well not my laptop but a laptop from pc
# the latency is alrite ig? idk if the laptop is using wifi 5 , probably is. 7pm

# def product_form(request):
#     if request.method =="POST":
#         # print(request.body)
#         # print(request.POST['name'])
#         name = request.POST['name']
#         obj = Category(name=name)
#         obj.save()
        
#     else:
#         print(request.method)


#     return render(request,'index.html')