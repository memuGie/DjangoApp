import os
import json
import traceback

from django.conf import settings

from .forms import ImageUploadingForm
from .models import User, PhotoInfo, Face
from .lib.app_logging.custom_logger import CustomLogger


logger = CustomLogger.get_instance()


def delete_file(file_url):
    image_url = os.path.join(os.path.dirname(settings.MEDIA_ROOT), file_url[1:])
    try:
        os.remove(image_url)
    except Exception:
        logger.error("File [%s] could not be deleted.Exc:\n%s" % (image_url, traceback.format_exc()))
    else:
        logger.debug("File [%s] has been deleted" % image_url)


def build_image_detail_path(img_url):
    filename, extension = os.path.splitext(img_url)
    return filename + "-detail" + extension


def handle_file_upload(request):
    upload_form = ImageUploadingForm(request.POST, request.FILES)
    if upload_form.is_valid():
        uploaded_photo = upload_form.save(commit=False)
        uploaded_photo.owner_ref = User.objects.get(username=request.user)
        upload_form.save()
        img_url = os.path.join(os.path.dirname(settings.MEDIA_ROOT), uploaded_photo.image.url[1:])
        img_info = _query_image_info(img_url)
        _save_image_info(uploaded_photo, img_info)
        return img_info


def _query_image_info(img_url):
    from .lib.visionapi import get_image_info

    logger.debug("Getting info for image: %s" % img_url)
    image_info = get_image_info(img_url)
    try:
        _apply_face_rectangles_pillow(img_url, image_info)
    except:
        logger.warning("Unable to mark faces on the image: %s\n%s" % (img_url, traceback.format_exc()))
    return image_info


def _save_image_info(photo, img_info):
    photo_info = json.loads(img_info)
    pi = _save_photo_info(photo, photo_info)
    _save_photo_faces(pi, photo_info['faces'])


def _save_photo_info(photo, photo_info):
    pi = PhotoInfo.objects.create(
        caption=photo_info['description']['captions'][0]['text'],
        tags=str(photo_info['description']['tags']),
        raw_json=json.dumps(photo_info),
        width=photo_info['metadata']['width'],
        height=photo_info['metadata']['height'],
        format=photo_info['metadata']['format'].lower(),
        photo_ref=photo)
    pi.save()
    return pi


def _save_photo_faces(photo_info, faces_list):
    for face in faces_list:
        f = Face.objects.create(
            age=face['age'],
            gender=face['gender'],
            top=face['faceRectangle']['top'],
            left=face['faceRectangle']['left'],
            width=face['faceRectangle']['width'],
            height=face['faceRectangle']['height'],
            photo_info_ref=photo_info)
        f.save()


def _apply_face_rectangles_pillow(img_url, img_info):
    from PIL import Image, ImageDraw

    im = Image.open(img_url)
    draw = ImageDraw.Draw(im)

    json_dict = json.loads(img_info)
    if "faces" in json_dict.keys():
        for face in json_dict['faces']:
            try:
                draw.rectangle(
                    [
                        (
                            face['faceRectangle']['left'],
                            face['faceRectangle']['top']
                        ),
                        (
                            face['faceRectangle']['left'] + face['faceRectangle']['width'],
                            face['faceRectangle']['top'] + face['faceRectangle']['height']
                        )
                    ],
                    outline="green", fill=None)
            except:
                logger.error(traceback.format_exc())
                continue
        else:
            # Add the patch to the Axes
            # ax.set_axis_off()
            im.save(build_image_detail_path(img_url))