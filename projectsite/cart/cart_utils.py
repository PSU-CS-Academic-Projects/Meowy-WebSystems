from .models import Cart, CartItem
from store.models import ProductVariant

def get_cart(request):
    cart_id = request.session.get('cart_id')
    cart = None
    if cart_id:
        try:
            cart = Cart.objects.prefetch_related('items__product_variant__product').get(id=cart_id)
        except Cart.DoesNotExist:
            cart = None
    
    if cart is None:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    return cart

def get_cart_items_count(request):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        return 0
    try:
        cart = Cart.objects.get(id=cart_id)
        return cart.get_total_items()
    except Cart.DoesNotExist:
        return 0
