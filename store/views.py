from django.shortcuts import render,redirect
from .models import Product,Category,Customer,Orders
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.hashers import make_password,check_password
from store.middlewares.auth import auth_middlewares
from django.utils.decorators import method_decorator
def index(request):
    if request.method == "POST":
        product = request.POST.get('product')
        cart = request.session.get('cart')
        remove=request.POST.get('remove')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]=quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart']=cart
        return redirect('index')
    else:
        cart=request.session.get('cart')
        if not cart:
            request.session.cart={}
        categories = Category.objects.all()
        products = None
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.objects.filter(category=categoryID)
        else:
            products = Product.objects.all()
        return render(request,'index.html',{'products':products,'categories':categories,'uname':request.session.get('username')})
def signup(request):
    if request.method=='GET':
      return render(request,'signup.html')
    else:
        postData=request.POST
        first_name=postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phonenum')
        email = postData.get('emailID')
        password=postData.get('password')
        value={
            'first_name':first_name,
            'last_name':last_name,
            'email':email,
            'phone':phone,
            'password':password
        }
        error_message=None
        if not first_name:
            error_message="First Name is required"
        elif not first_name.isalpha():
            error_message="First name cannot contains numbers"
        elif not last_name:
            error_message="Last Name is required"
        elif not first_name.isalpha():
            error_message="Last name cannot contains numbers"
        elif not phone:
            error_message="phone number is required"
        elif len(phone)<10:
            error_message="Invalid Phone Number"
        elif not phone.isdigit():
            error_message="Phone Number cannot contains characters"
        elif not email:
            error_message="Email id is required"
        elif email:
            exist=Customer.objects.filter(email=email)
            if exist:
                error_message="Email ID is already registerd"
            else:
                pass
        elif not password:
            error_message="Password is required"
        elif len(password)<8:
            error_message="Password should be of 8 characters"
        if not error_message:
            customer=Customer(first_name=first_name,last_name=last_name,phone=phone,email=email,password=password)
            customer.password=make_password(customer.password)
            customer.save()
            return redirect('index')
        else:
            return render(request,'signup.html',{'values':value,'error':error_message})



def valid(email):
    try:
        return Customer.objects.get(email=email)
    except:
        return False


return_url=None

def signin(request):
    global return_url
    if request.method == "GET":
        return_url=request.GET.get('returnurl')
        print(return_url)
        return render(request,'signin.html')
    else:
      error_message = None
      email=request.POST.get('emailID')
      password=request.POST.get('password')
      values={
          'email': email,
          'password': password
      }
      if not email:
        error_message = "Email id is required"
        return render(request,'signin.html',{'error':error_message,'value':values})
      elif not password:
        error_message = "password is required"
        return render(request, 'signin.html', {'error': error_message, 'value': values})
      else:
        customer = valid(email)
        if customer:
          flag = check_password(password, customer.password)
          if flag:
             request.session['customer']=customer.id
             request.session['username']=customer.first_name
             print(return_url)
             if return_url:
                 return HttpResponseRedirect(return_url)
             else:
                 return redirect('index')
          else:
             error_message="Invalid email or password"
             return render(request, 'signin.html', {'error': error_message, 'value': values})


def cart(request):
    if request.method=="GET":
        if request.session.get('cart'):
            ids=list(request.session.get('cart').keys())
            products=Product.objects.filter(id__in=ids)
            return render(request,'cart.html',{'cart':products})
        else:
            return render(request,'emptyCart.html')

@auth_middlewares
def fillDetails(request):
        customer=request.session.get('customer')
        details=Customer.objects.get(id=customer)
        ids=list(request.session.get('cart').keys())
        products=Product.objects.filter(id__in=ids)
        return render(request,'checkout.html',{'details':details,'products':products})


def logout(request):
    request.session.clear()
    return redirect("signin")


def checkOut(request):
    if request.method == "POST":
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        product_ids = list(request.session.get('cart').keys())
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            order = Orders(customer=Customer(id=customer),product=product,
                         price = product.price,quantity=cart.get(str(product.id)),
                         address = address,phone=phone)
            order.save()
        request.session['cart']={}
        return redirect('cart')


def orders(request):
    if request.method == 'GET':
        customer = request.session['customer']
        order = Orders.objects.filter(customer=customer).order_by('-price')
        return render(request,'orders.html',{'order':order})