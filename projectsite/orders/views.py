from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart_utils import get_cart
from django.contrib import messages
from django.db import transaction

def order_create(request):
    cart = get_cart(request)
    if cart.items.count() == 0:
        messages.error(request, "Your cart is empty. Add some products before checking out!")
        return redirect('store:product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            try:
                # Wrap in transaction to ensure either everything succeeds or everything rolls back
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.save()
                    
                    # Create OrderItem for each CartItem and update stock
                    for item in cart.items.all():
                        variant = item.product_variant
                        
                        # Validate stock one last time before purchase
                        if variant.stock < item.quantity:
                            raise ValueError(f"Insufficient stock for {variant.product.name} ({variant.flavor} - {variant.weight}). Only {variant.stock} left.")
                        
                        # Deduct stock
                        variant.stock -= item.quantity
                        variant.save()
                        
                        OrderItem.objects.create(
                            order=order,
                            product_variant=variant,
                            price_at_purchase=variant.price,
                            quantity=item.quantity
                        )
                    
                    # Delete the cart items and the cart itself to clear it
                    cart.delete()
                    if 'cart_id' in request.session:
                        del request.session['cart_id']
                
                messages.success(request, "Your order has been placed successfully!")
                request.session['placed_order_id'] = order.id
                return redirect('orders:order_success', order_id=order.id)
            
            except ValueError as e:
                messages.error(request, str(e))
                return redirect('cart:cart_detail')
    else:
        form = OrderCreateForm()
    
    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'form': form
    })

def order_success(request, order_id):
    # Only allow viewing the success page if this order was just placed in this session
    if request.session.get('placed_order_id') != order_id:
        messages.error(request, "You do not have permission to access that order details page.")
        return redirect('store:product_list')
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_success.html', {'order': order})
