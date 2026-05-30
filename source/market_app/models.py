from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, unique=True, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, verbose_name='Категория')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name='Стоимость')
    image = models.URLField(null=False, blank=False, verbose_name='Изображение')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'product'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'