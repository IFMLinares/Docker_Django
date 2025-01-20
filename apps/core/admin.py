from django.contrib import admin
from apps.core.models import Category, Product, Sale, DetSale
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(DetSale)

