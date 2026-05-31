from django.shortcuts import render, get_object_or_404, redirect
from market_app.models import Product, Category


def products_view(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'market_app/products.html', context)


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'market_app/product.html', context)


def product_add_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'market_app/product_add.html', context)
    elif request.method == 'POST':
        product = Product.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            category=Category.objects.get(id=request.POST.get('category')),
            price=request.POST.get('price'),
            image=request.POST.get('image'),
        )
        return redirect('product', pk=product.pk)

def category_add_view(request):
    if request.method == 'GET':
        return render(request, 'market_app/category_add.html')
    elif request.method == 'POST':
        Category.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
        )
        return redirect('products')