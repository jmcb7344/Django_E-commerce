from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


user = get_user_model()

class Product(models.Model):
    """
    Gestiona los productos de nuesta E-commerce
    """
    name = models.CharField(max_length=70)
    brand = models.CharField(max_length=50, help_text='Marca del producto')
    slug = models.SlugField(max_length=50)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    active = models.BooleanField(default=False)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        ordering = ['-active', '-created']

    def __str__(self):
        return f'{self.name} - Marca {self.brand} - Active = {self.active}'

    @property #El properti convertir un metodo en en una propiedad, objeto.metodo, en vez de objeto.metodo()
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug':self.slug})

class Order(models.Model):
    """Pedido que mostrara el carrito"""
    client = models.ForeignKey(user, on_delete=models.CASCADE)
    date_order = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False, null=True, blank=False)
    transaccion_id = models.CharField(max_length=70, null=True)

    def __str__(self) -> str:
        return f'{self.user} - {self.transaccion_id}'

    @property
    def get_cart_total(self):
        product_item = self.orderitem.set.all()
        total = sum([item.get_total for item in product_item])
        return total

    @property
    def get_cart_item(self):
        product_item = self.orderitem.set.all()
        total = sum([item.quantity for item in product_item])
        return total

class OrderItem(models.Model):
    """Contendra el producto y a que order pertenece"""
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total