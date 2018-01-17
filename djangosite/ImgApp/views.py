import os
import traceback

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Photo, User
from .forms import ImageUploadingForm
from .app_logging.custom_logger import CustomLogger

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
    try:
        _apply_face_rectangles(img_url, image_info)
    except:
        logger.warning("Unable to mark faces on the image: %s\n%s" % (img_url, traceback.format_exc()))
    return image_info


def _apply_face_rectangles(img_url, img_info):
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from PIL import Image
    import numpy as np
    import json
    import time

    im = np.array(Image.open(img_url), dtype=np.uint8)
    # Create figure and axes
    fig, ax = plt.subplots(1)

    # Display the image
    ax.imshow(im)
    json_dict = json.loads(img_info)
    if "faces" in json_dict.keys():
        for face in json_dict['faces']:
            try:
                # Create a Rectangle patch
                rect = patches.Rectangle(
                    (face['faceRectangle']['left'], face['faceRectangle']['top']),
                    face['faceRectangle']['width'],
                    face['faceRectangle']['height'],
                    linewidth=1, edgecolor='g', facecolor='none')
                ax.add_patch(rect)
                time.sleep(1)
            except:
                logger.error(traceback.format_exc())
                continue
        else:
            # Add the patch to the Axes
            # ax.set_axis_off()
            filename, extension = os.path.splitext(img_url)
            plt.savefig(filename + "-detail" + extension,
                        bbox_inches='tight',
                        pad_inches=0,
                        dpi=600)
