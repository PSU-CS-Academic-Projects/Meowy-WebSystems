from .cart_utils import get_cart_items_count

def cart_info(request):
    return {
        'cart_count': get_cart_items_count(request)
    }
