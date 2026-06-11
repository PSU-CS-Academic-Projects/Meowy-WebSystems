from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product_variant']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'email', 'phone', 'payment_method', 'paid', 'created_at']
    list_filter = ['paid', 'created_at', 'payment_method']
    search_fields = ['customer_name', 'email', 'phone', 'address']
    inlines = [OrderItemInline]
