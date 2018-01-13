from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Photo(models.Model):
    name = models.CharField(max_length=100, default="photo")
    upload_date = models.DateTimeField(verbose_name='date uploaded', default=timezone.now)
    owner_ref = models.OneToOneField(
        User, default=User.objects.get(username='root').pk, on_delete=models.DO_NOTHING)
    image = models.ImageField()
