from .app_logging.custom_logger import CustomLogger

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Photo, User
from .forms import ImageUploadingForm

#TODO: fix Django logging in order not to use the CustomLogger -> settings.py
logger = CustomLogger.get_instance()


def index(request):
    import os
    from django.conf import settings
    from .lib.visionapi import get_image_info

    if not request.user.is_authenticated:
        return HttpResponse("""Please <a href="login">login</a>...""")
    if request.method == "POST":
        _handle_file_upload(request)
    logger.info("User %s has logged in" % request.user)
    user_photos = Photo.objects.filter(
        owner_ref=User.objects.get(username=request.user)).order_by("upload_date").reverse()
    form = ImageUploadingForm()
    image_info = ""
    if user_photos:
        print(settings.BASE_DIR)
        print(settings.MEDIA_ROOT)
        print(os.path.dirname(settings.MEDIA_ROOT))
        print(os.path.join(os.path.dirname(settings.MEDIA_ROOT), user_photos[0].image.url[1:]))
        print(user_photos[0].image.url)

        image_info = get_image_info(
            os.path.join(os.path.dirname(settings.MEDIA_ROOT), user_photos[0].image.url[1:]))
    context = {'user_photos': user_photos, 'form': form, 'image_info': image_info}

    return render(request, "ImgApp/index.html", context)


def _handle_file_upload(request):
    upload_form = ImageUploadingForm(request.POST, request.FILES)
    if upload_form.is_valid():
        uploaded_photo = upload_form.save(commit=False)
        uploaded_photo.owner_ref = User.objects.get(username=request.user)
        upload_form.save()
        return HttpResponseRedirect("ImgApp/index.html")
