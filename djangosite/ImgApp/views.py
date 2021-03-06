from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .services import *
from .forms import ImageUploadingForm
from . import view_functions
from .lib.app_logging.custom_logger import CustomLogger

#TODO: fix Django logging in order not to use the CustomLogger -> settings.py
logger = CustomLogger.get_instance()


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/ImgApp/login")
    if request.method == "POST":
        view_functions.handle_file_upload(request.POST, request.FILES, request.user)
    user_photos = get_user_photos_latest_first(user=request.user)
    form = ImageUploadingForm()
    context = {'user_photos': user_photos, 'form': form}

    return render(request, "ImgApp/index.html", context)


@login_required
def photo_detail(request, user_photo_id):
    user_photo = get_photo_by_id(user_photo_id)
    img_url = user_photo.image.url
    detail_photo_url = view_functions.build_image_detail_path(img_url)
    context = {'detail_photo_url': detail_photo_url, 'user_photo': user_photo}
    return render(request, "ImgApp/detail.html", context)


@login_required
def photo_delete(request, user_photo_id):
    photo_to_delete = get_photo_by_id(user_photo_id)
    photo_to_delete.delete()
    view_functions.delete_file(photo_to_delete.image.url)
    view_functions.delete_file(view_functions.build_image_detail_path(photo_to_delete.image.url))
    return HttpResponseRedirect("/ImgApp")
