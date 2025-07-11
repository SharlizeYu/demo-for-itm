from .models import Product, CartItem
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

@login_required
def product_detail(request, product_id):
    if request.method == 'GET':
        template = loader.get_template("core/product_detail.html")
        p = Product.objects.get(id=product_id)
        context = {
            "product": p
        }
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        submitted_quantity = request.POST['quantity']
        submitted_product_id = request.POST['product_id']
        product = Product.objects.get(id=submitted_product_id)
        user = request.user
        cart_item = CartItem(user=user, product=product, 
quantity=submitted_quantity)
        cart_item.save()
        messages.add_message(
            request,
            messages.INFO,
            f'Added {submitted_quantity} of {product.name} to your cart'
        )
        return redirect('index')

from .models import Transaction, LineItem

@login_required
def transaction_history(request):
    transactions = 
Transaction.objects.filter(user=request.user).order_by('-created_at')
    history = []
    for transaction in transactions:
        items = LineItem.objects.filter(transaction=transaction)
        history.append({
            "transaction": transaction,
            "items": items
        })
    template = loader.get_template("core/transaction_history.html")
    context = {
        "history": history,
    }
    return HttpResponse(template.render(context, request))

