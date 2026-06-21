from django.core.validators import MinValueValidator
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
    price = models.DecimalField(max_digits=7, decimal_places=2, null=False, verbose_name='Стоимость')
    image = models.URLField(null=False, blank=False, verbose_name='Изображение')
    stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Остаток'
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'product'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class CartItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Количество'
    )

    def __str__(self):
        return f'{self.product.title} x{self.quantity}'

    def get_total(self):
        return self.product.price * self.quantity

    class Meta:
        db_table = 'cart_item'
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'


class Order(models.Model):
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name='Имя'
    )
    phone = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        verbose_name='Телефон'
    )
    address = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        verbose_name='Адрес'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    products = models.ManyToManyField(
        Product,
        through='OrderItem',
        verbose_name='Товары'
    )

    def __str__(self):
        return f'Заказ №{self.pk} - {self.name}'

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Количество'
    )

    def __str__(self):
        return f'{self.product.title} x{self.quantity}'

    class Meta:
        db_table = 'order_item'
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'