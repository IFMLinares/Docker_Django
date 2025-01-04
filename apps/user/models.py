from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings

# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)

    # Metodo para obtener la URL de la imagen
    def get_image_url(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return ''