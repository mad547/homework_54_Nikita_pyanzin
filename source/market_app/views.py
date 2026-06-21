from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from market_app.models import Product, Category, CartItem, Order, OrderItem
from market_app.forms import ProductForm, CategoryForm, OrderForm

class ProductListView(ListView):
    template_name = 'market_app/products.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        queryset = Product.objects.filter(
            stock__gte=1
        ).order_by('category__title', 'title')

        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context


class ProductDetailView(DetailView):
    template_name = 'market_app/product.html'
    model = Product
    context_object_name = 'product'


class ProductCreateView(CreateView):
    template_name = 'market_app/product_add.html'
    form_class = ProductForm
    model = Product

    def get_success_url(self):
        return reverse_lazy('product', kwargs={'pk': self.object.pk})


class ProductUpdateView(UpdateView):
    template_name = 'market_app/product_edit.html'
    form_class = ProductForm
    model = Product
    context_object_name = 'product'

    def get_success_url(self):
        return reverse_lazy('product', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    template_name = 'market_app/product_confirm_delete.html'
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('products')


class CategoryCreateView(CreateView):
    template_name = 'market_app/category_add.html'
    form_class = CategoryForm
    model = Category
    success_url = reverse_lazy('products')


class CategoryProductsView(ListView):
    template_name = 'market_app/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = Category.objects.get(title=self.kwargs.get('category_title'))
        return Product.objects.filter(
            category=self.category, stock__gte=1
        ).order_by('title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class CartView(ListView):
    template_name = 'market_app/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return CartItem.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = CartItem.objects.all()
        context['total'] = sum(item.get_total() for item in items)
        context['form'] = OrderForm()
        return context


class CartAddView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.stock < 1:
            return redirect('products')
        cart_item = CartItem.objects.filter(product=product).first()
        if cart_item:
            if cart_item.quantity < product.stock:
                cart_item.quantity += 1
                cart_item.save()
        else:
            CartItem.objects.create(product=product, quantity=1)
        return redirect('products')


class CartRemoveView(View):
    def post(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk)
        cart_item.delete()
        return redirect('cart')


class OrderCreateView(View):
    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
            )
            cart_items = CartItem.objects.all()
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                )
            cart_items.delete()
            return redirect('products')
        cart_items = CartItem.objects.all()
        total = sum(item.get_total() for item in cart_items)
        return render(request, 'market_app/cart.html', {
            'cart_items': cart_items,
            'total': total,
            'form': form,
        })