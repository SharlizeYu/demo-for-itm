from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import Product, CartItem  # Ensure CartItem is imported
from .models import Transaction
@login_required
def index(request):
    template = loader.get_template("core/index.html")
    products = Product.objects.all()
    context = {
        "user": request.user,
        "product_data": products
    }
    return HttpResponse(template.render(context, request))

@login_required
def product_detail(request, product_id):
    if request.method == 'GET':
        template = loader.get_template("core/product_detail.html")
        product = Product.objects.get(id=product_id)
        context = {
            "product": product
        }
        return HttpResponse(template.render(context, request))

    elif request.method == 'POST':
        submitted_quantity = request.POST['quantity']
        submitted_product_id = request.POST['product_id']
        product = Product.objects.get(id=submitted_product_id)
        user = request.user

        # Create and save CartItem
        cart_item = CartItem(user=user, product=product, quantity=submitted_quantity)
        cart_item.save()

        # Add message to show on index page
        messages.add_message(
            request,
            messages.INFO,
            f'Added {submitted_quantity} of {product.name} to your cart'
        )

        return redirect('index')

def login_view(request):
    if request.method == 'GET':
        template = loader.get_template("core/login_view.html")
        context = {}
        return HttpResponse(template.render(context, request))

    elif request.method == 'POST':
        submitted_username = request.POST['username']
        submitted_password = request.POST['password']
        user_object = authenticate(
            username=submitted_username,
            password=submitted_password
        )
        if user_object is None:
            messages.add_message(request, messages.INFO, 'Invalid login.')
            template = loader.get_template("core/login_view.html")
            return HttpResponse(template.render({}, request))
        else:
            login(request, user_object)
            return redirect('index')

import datetime as dt
from .models import Transaction, LineItem, CartItem

@login_required
def checkout(request):
    if request.method == 'GET':
        template = loader.get_template("core/checkout.html")
        cart_items = CartItem.objects.filter(user=request.user)
        context = {
            'cart_items': list(cart_items),
            'user': request.user
        }
        return HttpResponse(template.render(context, request))

    elif request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        created_at = dt.datetime.now(tz=dt.timezone.utc)
        transaction = Transaction(user=request.user, 
created_at=created_at)
        transaction.save()
        for cart_item in cart_items:
            line_item = LineItem(
                transaction=transaction,
                product=cart_item.product,
                quantity=cart_item.quantity,
            )
            line_item.save()
            cart_item.delete()
        messages.add_message(request, messages.INFO, f'Thank you for your purchase!')
        return redirect('index')


@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
    template = loader.get_template("core/transaction_history.html")
    context = {
        "user": request.user,
        "transactions": transactions
    }
    return HttpResponse(template.render(context, request))
