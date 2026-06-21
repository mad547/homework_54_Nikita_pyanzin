from multiprocessing import context

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from market_app.models import Product, Category
from market_app.forms import ProductForm, CategoryForm

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
    template_name = 'market_app/products.html'
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
    success_url = reverse_lazy('product')


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