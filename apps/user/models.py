from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.forms import model_to_dict

from django.conf import settings

# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)

    # Metodo para obtener la URL de la imagen
    def get_image_url(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return ''
    
    def toJson(self):
        item = model_to_dict(self, exclude=['password', 'groups', 'user_permissions', 'last_login'])
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%Y-%m-%d') if self.last_login else ''

        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d') if self.date_joined else ''
        item['image'] = self.get_image_url()
        return item
    
    def get_update_url(self):
        return reverse('user:user_update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('user:user_delete', kwargs={'pk': self.pk})

    # def save(self, *args, **kwargs):
    #     if self.pk is not None:
    #         self.set_password(self.password)
    #     else:
    #         user = User.objects.get(pk=self.pk)
    #         if user.password != self.password:
    #             self.set_password(self.password)
    #     super().save(*args, **kwargs)