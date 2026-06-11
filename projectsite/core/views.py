from django.shortcuts import render, redirect
from store.models import Product, Category
from django.db.models import Min
from .forms import ContactForm
from django.contrib import messages

def home(request):
    categories = Category.objects.all()
    # Annotate products with their minimum variant price and grab first 6 for features
    featured_products = Product.objects.annotate(min_price=Min('variants__price'))[:6]
    
    return render(request, 'core/home.html', {
        'categories': categories,
        'featured_products': featured_products,
    })

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # In a real app we'd send an email. For this MVP, we will show a success message.
            messages.success(request, f"Thank you, {form.cleaned_data['name']}! Your message has been sent. We'll get back to you soon.")
            return redirect('core:contact')
    else:
        form = ContactForm()
        
    return render(request, 'core/contact.html', {'form': form})
