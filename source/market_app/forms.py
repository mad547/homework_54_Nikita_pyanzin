from django.forms import ModelForm, widgets
from django.core.validators import MinValueValidator
from market_app.models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'image','category', 'description', 'stock']
        widgets = {
            'title': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
            'price': widgets.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена'}),
            'image': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ссылка на изображение'}),
            'category': widgets.Select(attrs={'class': 'form-control'}),
            'description':widgets.Textarea(attrs={'class': 'form-control', 'rows': '4', 'placeholder': 'Описание'}),
            'stock': widgets.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Остаток', 'min': '0'}),
        }