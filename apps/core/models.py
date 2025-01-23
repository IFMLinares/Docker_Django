from django.db import models
from datetime import datetime
from django.urls import reverse
from django.forms import model_to_dict
from django.conf import settings

from crum import get_current_user

from apps.core.choices import gender_choices

from apps.models import BaseModel

# Create your models here.
class Category(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=255, null=True, blank=True, verbose_name='Descripción')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        return super(Category, self).save()
    
    # Método para obtener la informacion en Json
    def to_json(self):
        item = model_to_dict(self)
        return item
    
    # Método para obtener la URL de actualización
    def get_update_url(self):
        return reverse('core:category_edit', kwargs={'pk': self.pk})

    # Método para obtener la URL de eliminación
    def get_delete_url(self):
        return reverse('core:category_delete', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    cate = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True)
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.name
    
    def toJson(self):
        item = model_to_dict(self)
        item['cate'] = self.cate.to_json()
        item['image'] = self.get_image_url()
        item['pvp'] = format(self.pvp, '.2f')
        return item

    # Método para obtener la URL de actualización
    def get_update_url(self):
        return reverse('core:product_edit', kwargs={'pk': self.pk})

    # Método para obtener la URL de eliminación
    def get_delete_url(self):
        return reverse('core:product_delete', kwargs={'pk': self.pk})
    
    # Metodo para obtener la URL de la imagen
    def get_image_url(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return ''

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']

class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos')
    dni = models.CharField(max_length=10, unique=True, verbose_name='Dni')
    date_birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')

    def __str__(self):
        return self.names
    
    def toJson(self):
        item = model_to_dict(self)
        item['gender'] = self.get_gender_display()
        item['date_birthday'] = self.date_birthday.strftime('%Y-%m-%d')
        return item

    def get_update_url(self):
        return reverse('core:client_edit', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('core:client_delete', kwargs={'pk': self.pk})

    def get_image_url(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return ''

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']

class Sale(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def get_update_url(self):
        return reverse('core:sale_edit', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('core:sale_delete', kwargs={'pk': self.pk})

    def toJson(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJson()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['det'] = [i.toJson() for i in self.detsale_set.all()]

    def __str__(self):
        return self.cli.names

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']

class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJson(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJson()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']
