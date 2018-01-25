from django.contrib.auth.models import User

from .models import Photo


def get_photo_by_id(photo_id):
    return Photo.objects.get(pk=photo_id)


def get_user_photos_latest_first(user):
    return Photo.objects.filter(
        owner_ref=User.objects.get(username=user)).order_by("upload_date").reverse()