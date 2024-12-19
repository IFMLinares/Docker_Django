from django.db import models
from django.forms import model_to_dict

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=255, null=True, blank=True, verbose_name='Descripción')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    # Método para obtener la informacion en Json
    def to_json(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']