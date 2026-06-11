from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import ProductVariant
from .models import Cart, CartItem
from .cart_utils import get_cart
from django.contrib import messages

def cart_detail(request):
    cart = get_cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@require_POST
def cart_add(request):
    cart = get_cart(request)
    variant_id = request.POST.get('variant_id')
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1
        
    if quantity < 1:
        messages.error(request, "Quantity must be at least 1.")
        return redirect('store:product_list')
    
    variant = get_object_or_404(ProductVariant, id=variant_id)
    
    # Check variant stock
    if variant.stock < quantity:
        messages.error(request, f"Sorry, only {variant.stock} item(s) available for {variant}.")
        return redirect('store:product_detail', id=variant.product.id)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product_variant=variant)
    if not created:
        # Check total stock if adding more
        new_qty = cart_item.quantity + quantity
        if variant.stock < new_qty:
            messages.error(request, f"Cannot add more items. Only {variant.stock} available.")
            return redirect('store:product_detail', id=variant.product.id)
        cart_item.quantity = new_qty
    else:
        cart_item.quantity = quantity
    
    cart_item.save()
    messages.success(request, f"Added {variant} to your cart.")
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, item_id):
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    messages.info(request, f"Removed {cart_item.product_variant} from your cart.")
    cart_item.delete()
    return redirect('cart:cart_detail')

@require_POST
def cart_update(request, item_id):
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1
        
    if quantity < 1:
        quantity = 1
    
    # Check variant stock
    variant = cart_item.product_variant
    if variant.stock < quantity:
        messages.error(request, f"Sorry, only {variant.stock} item(s) available for {variant}.")
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f"Updated quantity for {variant} to {quantity}.")
    return redirect('cart:cart_detail')
