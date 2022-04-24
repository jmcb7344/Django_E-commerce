import django
from django.contrib.auth import get_user_model
from django.utils.text import slugify
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
    image = models.ImageField()
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    active = models.BooleanField(default=False)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        ordering = ['-active', '-created']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - Marca {self.brand} - Active = {self.active}'

    #El properti convertir un metodo en en una propiedad, objeto.metodo, en vez de objeto.metodo()
    @property 
    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug':self.slug})

class Order(models.Model):
    """Pedido que mostrara el carrito"""
    client = models.ForeignKey(user, on_delete=models.CASCADE, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False, null=True, blank=False)
    transaccion_id = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'ORDER-{self.id} - {self.client} - {self.transaccion_id}'

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='item', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total

    def get_cart_total(self):
        product_item = self.orderitem.set.all()
        total = sum([item.get_total for item in product_item])
        return total