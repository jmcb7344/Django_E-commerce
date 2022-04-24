from django.contrib import admin
from catalog import models

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)