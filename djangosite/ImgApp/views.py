from .app_logging.custom_logger import CustomLogger

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Photo, User
from .forms import ImageUploadingForm

#TODO: fix Django logging in order not to use the CustomLogger -> settings.py
logger = CustomLogger.get_instance()


def index(request):
    if not request.user.is_authenticated:
        return HttpResponse("""Please <a href="login">login</a>...""")

    logger.info("User %s has logged in" % request.user)
    img_info = ""
    if request.method == "POST":
        img_info = _handle_file_upload(request)
    user_photos = Photo.objects.filter(
        owner_ref=User.objects.get(username=request.user)).order_by("upload_date").reverse()
    form = ImageUploadingForm()
    context = {'user_photos': user_photos, 'form': form, 'image_info': img_info}

    return render(request, "ImgApp/index.html", context)


def _handle_file_upload(request):
    import os
    from django.conf import settings

    upload_form = ImageUploadingForm(request.POST, request.FILES)
    if upload_form.is_valid():
        uploaded_photo = upload_form.save(commit=False)
        uploaded_photo.owner_ref = User.objects.get(username=request.user)
        upload_form.save()
        img_url = os.path.join(os.path.dirname(settings.MEDIA_ROOT), uploaded_photo.image.url[1:])
        return _query_image_info(img_url)


def _query_image_info(img_url):
    from .lib.visionapi import get_image_info

    logger.debug("Getting info for image: %s" % img_url)
    image_info = get_image_info(img_url)
    return image_info
