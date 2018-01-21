from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import Photo, User
from .forms import ImageUploadingForm
from . import view_functions
from .lib.app_logging.custom_logger import CustomLogger

#TODO: fix Django logging in order not to use the CustomLogger -> settings.py
logger = CustomLogger.get_instance()


def index(request):
    if not request.user.is_authenticated:
        return HttpResponse("""Please <a href="login">login</a>...""")
    if request.method == "POST":
        view_functions.handle_file_upload(request)
    user_photos = Photo.objects.filter(
        owner_ref=User.objects.get(username=request.user)).order_by("upload_date").reverse()
    form = ImageUploadingForm()
    context = {'user_photos': user_photos, 'form': form}

    return render(request, "ImgApp/index.html", context)


@login_required
def photo_detail(request, user_photo_id):
    user_photo = Photo.objects.get(pk=user_photo_id)
    img_url = user_photo.image.url
    detail_photo_url = view_functions.build_image_detail_path(img_url)
    context = {'detail_photo_url': detail_photo_url, 'user_photo': user_photo}
    return render(request, "ImgApp/detail.html", context)


@login_required
def photo_delete(request, user_photo_id):
    photo_to_delete = Photo.objects.get(pk=user_photo_id)
    photo_to_delete.delete()
    view_functions.delete_file(photo_to_delete.image.url)
    view_functions.delete_file(view_functions.build_image_detail_path(photo_to_delete.image.url))
    return HttpResponseRedirect("/ImgApp")
