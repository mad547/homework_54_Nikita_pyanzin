from django.shortcuts import render, get_object_or_404, redirect
from market_app.models import Product, Category
from market_app.forms import ProductForm, CategoryForm


def products_view(request):
    products = Product.objects.filter(stock__gte=1).order_by('category__title', 'title')
    context = {'products': products}
    return render(request, 'market_app/products.html', context)


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'market_app/product.html', context)


def product_add_view(request):
    form = ProductForm()
    if request.method == 'GET':
        return render(request, 'market_app/product_add.html', {'form': form})
    elif request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('product', pk=product.pk)
    return render(request, 'market_app/product_add.html', {'form': form})


def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(instance=product)
    if request.method == 'GET':
        return render(request, 'market_app/product_edit.html', {'form': form, 'product': product})
    elif request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product', pk=product.pk)
        return render(request, 'market_app/product_edit.html', {'form': form, 'product': product})


def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    return render(request, 'market_app/product_confirm_delete.html', {'product': product})


def category_add_view(request):
    form = CategoryForm()
    if request.method == 'GET':
        return render(request, 'market_app/category_add.html', {'form': form})
    elif request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
        return render(request, 'market_app/category_add.html', {'form': form})


def category_products_view(request, category_title):
    category = get_object_or_404(Category, title=category_title)
    products = Product.objects.filter(
        category=category, stock__gte=1
    ).order_by('title')
    context = {'products': products, 'category': category}
    return render(request, 'market_app/category_products.html', context)