from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from .models import Category, Brand, Product, ProductAttribute, CartOrder, OrderItems, Wishlist
from django.template.loader import render_to_string
from . forms import SignupForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from sslcommerz_lib import SSLCOMMERZ
from django.contrib import messages


def home(request):
    product = Product.objects.filter(is_featured=True)
    return render(request, 'index.html', {'product': product})


def search(request):
    if request.method == 'GET':
        search = request.GET['search']
        if search != '':
            product = Product.objects.filter(title__icontains=search)
            return render(request, 'search.html', {'product': product})
        else:
            product = Product.objects.filter(is_featured=True)
    return render(request, 'index.html', {'product': product})


def product(request):
    total_product = Product.objects.count()
    product = Product.objects.all()[:3]

    return render(request, 'product/products.html', {'product': product, 'totalProduct': total_product})


def product_details(request, slug, id):
    product = Product.objects.get(id=id)
    related = Product.objects.filter(
        category=product.category).exclude(id=id)[:2]
    color = ProductAttribute.objects.filter(product=product).values(
        'color__id', 'color__title', 'color__color_code').distinct()
    size = ProductAttribute.objects.filter(product=product).values(
        'size__id', 'size__title', 'price', 'color__id').distinct()
    return render(request, 'product/product_details.html', {'product': product, 'related': related, 'color': color, 'size': size})


def category(request):
    category = Category.objects.all()

    return render(request, 'category/categories.html', {'category': category})


def category_products(request, id):
    category = Category.objects.get(id=id)
    product = Product.objects.filter(category=category)
    return render(request, 'category/category_products.html', {'product': product})


def brands(request):
    brand = Brand.objects.all()
    return render(request, 'brand/brands.html', {'brand': brand})


def brand_products(request, id):
    brand = Brand.objects.get(id=id)
    product = Product.objects.filter(brand=brand)
    return render(request, 'brand/brand_products.html', {'product': product})


def filter_data(request):
    colors = request.GET.getlist('color[]')
    sizes = request.GET.getlist('size[]')
    brands = request.GET.getlist('brand[]')
    categories = request.GET.getlist('category[]')
    allProducts = Product.objects.all()
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']
    allProducts = allProducts.filter(productattribute__price__gte=minPrice)
    allProducts = allProducts.filter(productattribute__price__lte=maxPrice)

    if len(colors) > 0:
        allProducts = allProducts.filter(
            productattribute__color__id__in=colors).distinct()
    if len(sizes) > 0:
        allProducts = allProducts.filter(
            productattribute__size__id__in=sizes).distinct()
    if len(brands) > 0:
        allProducts = allProducts.filter(brand__id__in=brands).distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(
            category__id__in=categories).distinct()

    tem = render_to_string('ajax/products.html', {'product': allProducts})

    return JsonResponse({'data': tem})


def load_more(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    product = Product.objects.all()[offset:offset+limit]

    tem = render_to_string('ajax/products.html', {'product': product})

    return JsonResponse({'data': tem})


def add_to_cart(request):
    # del request.session['cartData']
    cart = {}
    cart[str(request.GET['id'])] = {
        'title': request.GET['product_title'],
        'image': request.GET['image'],
        'qty': request.GET['qty'],
        'price': request.GET['price']
    }

    if 'cartData' in request.session:
        if str(request.GET['id']) in request.session['cartData']:
            cart_data = request.session['cartData']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_data[str(
                request.GET['id'])]['qty']) + int(cart[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartData'] = cart_data
        else:
            cart_data = request.session['cartData']
            cart_data.update(cart)
            request.session['cartData'] = cart_data
    else:
        request.session['cartData'] = cart

    # tem = render_to_string('ajax/products.html', {'product':product})

    return JsonResponse({'data': request.session['cartData'], 'total': len(request.session['cartData'])})


def cart_list(request):
    total_amount = 0
    if 'cartData' in request.session:
        for p_id, item in request.session['cartData'].items():
            total_amount += int(item['qty'])*float(item['price'])
        return render(request, 'cart.html', {'data': request.session['cartData'], 'total': len(request.session['cartData']), 'total_amount': total_amount})
    return render(request, 'cart.html')


def delete_cart_item(request):
    if 'cartData' in request.session:
        if str(request.GET['id']) in request.session['cartData']:
            cart_data = request.session['cartData']
            del request.session['cartData'][str(request.GET['id'])]
            request.session['cartData'] = cart_data

    total_amount = 0
    for p_id, item in request.session['cartData'].items():
        total_amount += float(item['price']) * int(item['qty'])

    tem = render_to_string('ajax/cart_list.html', {'data': request.session['cartData'], 'total': len(
        request.session['cartData']), 'total_amount': total_amount})

    return JsonResponse({'data': tem, 'total': len(request.session['cartData'])})


def update_cart_item(request):
    pQty = request.GET['qty']
    id = str(request.GET['id'])

    if 'cartData' in request.session:
        if id in request.session['cartData']:
            cart_data = request.session['cartData']
            cart_data[str(request.GET['id'])]['qty'] = pQty
            # cart_data.update(cart_data)
            request.session['cartData'] = cart_data

    total_amount = 0
    for p_id, item in request.session['cartData'].items():
        total_amount += float(item['price']) * int(item['qty'])

    tem = render_to_string('ajax/cart_list.html', {'data': request.session['cartData'], 'total': len(
        request.session['cartData']), 'total_amount': total_amount})

    return JsonResponse({'data': tem, 'total': len(request.session['cartData'])})


def signup(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        print(fname)
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist")
            return redirect('signup')
        
        if len(username)>10:
            messages.error(request, "Username must less then 10 character")
            return redirect('signup')
        
        if not username.isalnum():
            messages.error(request, "Username only contain alphanumeric")
            return redirect('signup')
        
        if User.objects.filter(email=email):
            messages.error(request, "This email already have an account")
            return redirect('signup')
        
        if pass1!=pass2:
            messages.error(request, "Password didn't match")
            return redirect('signup')
        
        user = User.objects.create_user(username, email, pass1)
        user.first_name = fname
        user.last_name = lname

        user.save()
        return redirect('login')
    return render(request, 'registration/signup.html')


@login_required
def checkout(request):
    total_amnt = 0
    if request.method == "POST":
        name=request.POST['name'],
        email=request.POST['email'],
        mobile=request.POST['contact'],
        address=request.POST['address'],
        
        if 'cartData' in request.session:
            for p_id, item in request.session['cartData'].items():
                total_amnt += float(item['price']) * int(item['qty'])

            order = CartOrder.objects.create(
                user=request.user,
                name=name,
                email=email,
                mobile=mobile,
                address=address,
                tran_id='tran-123',
                total_amount=total_amnt
            )
            for p_id, item in request.session['cartData'].items():
                items = OrderItems.objects.create(
                    order=order,
                    invoice='INV-'+str(order.id),
                    item=item['title'],
                    image=item['image'],
                    qty=item['qty'],
                    price=item['price'],
                    total=float(item['qty'])*float(item['price'])
                )
                
        sslcz = SSLCOMMERZ({'store_id': 'ecomm642ab791870c9',
                        'store_pass': 'ecomm642ab791870c9@ssl', 'issandbox': True})

        post_body = {}
        post_body['total_amount'] = total_amnt
        post_body['currency'] = "BDT"
        post_body['tran_id'] = "12345"
        post_body['success_url'] = "http://127.0.0.1:8000/payment-done/"
        post_body['fail_url'] = "your fail url"
        post_body['cancel_url'] = "http://127.0.0.1:8000/payment-cancelled/"
        post_body['emi_option'] = 0
        post_body['cus_name'] = request.user
        post_body['cus_email'] = "test@test.com"
        post_body['cus_phone'] = "01700000000"
        post_body['cus_add1'] = "customer address"
        post_body['cus_city'] = "Dhaka"
        post_body['cus_country'] = "Bangladesh"
        post_body['shipping_method'] = "NO"
        post_body['multi_card_name'] = ""
        post_body['num_of_item'] = 1
        post_body['product_name'] = "Test"
        post_body['product_category'] = "Test Category"
        post_body['product_profile'] = "general"

        response = sslcz.createSession(post_body)  # API response
        return redirect(response['GatewayPageURL'])

    if 'cartData' in request.session:
        for p_id, item in request.session['cartData'].items():
            total_amnt += float(item['price']) * int(item['qty'])
        
    return render(request, 'checkout.html', {'data': request.session['cartData'], 'total': len(request.session['cartData']), 'total_amount': total_amnt})


@csrf_exempt
def payment_done(request):
    
    returnData = request.POST
    return render(request, 'payment-success.html', {'data': returnData})


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment-fail.html')


def dashboard(request):
    return render(request, 'user/dashboard.html')


def orders(request):
    orders = CartOrder.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/orders.html', {'orders': orders})


def orders_item(request, id):
    order = CartOrder.objects.get(pk=id)
    ordersItem = OrderItems.objects.filter(order=order).order_by('-id')
    return render(request, 'user/orders-items.html', {'ordersItem': ordersItem})


def add_wishlist(request):
    p_id = request.GET['product']
    product = Product.objects.get(pk=p_id)

    data = {}
    wish = Wishlist.objects.filter(user=request.user, product=product)

    if wish:
        data = {
            'bool': False
        }
    else:
        wishlist = Wishlist.objects.create(
            user=request.user,
            product=product
        )
        data = {
            'bool': True
        }

    return JsonResponse(data)


def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/wishlist.html', {'wishlist': wishlist})


def delete_wish_item(request):
    id = request.GET['id']
    data = Wishlist.objects.get(product=id)
    data.delete()
    
    wishlist = Wishlist.objects.filter(user=request.user).order_by('-id')

    tem = render_to_string('ajax/wish.html', {'wishlist': wishlist})

    return JsonResponse({'data': tem})


def pass_reset(request):
    return render(request, 'user/password_reset.html')

