from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Photo(models.Model):
    description = models.CharField(max_length=100, default="photo")
    upload_date = models.DateTimeField(verbose_name="date uploaded", default=timezone.now)
    owner_ref = models.ForeignKey(
        User, default=User.objects.get(username="root").pk, on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to="app_photos")

    @staticmethod
    def get_photo_by_id(photo_id):
        return Photo.objects.get(pk=photo_id)

    @staticmethod
    def get_user_photos_latest_first(user):
        return Photo.objects.filter(
            owner_ref=User.objects.get(username=user)).order_by("upload_date").reverse()


class PhotoInfo(models.Model):
    caption = models.CharField(max_length=200)
    tags = models.TextField()
    raw_json = models.TextField()
    width = models.IntegerField()
    height = models.IntegerField()
    format = models.CharField(max_length=10)
    photo_ref = models.OneToOneField(Photo, on_delete=models.CASCADE)


class Face(models.Model):
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    top = models.IntegerField()
    left = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    photo_info_ref = models.ForeignKey(PhotoInfo, on_delete=models.CASCADE, null=True, default=None)
