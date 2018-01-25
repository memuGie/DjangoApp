import os
import json
import traceback

from django.conf import settings

from .models import User
from .forms import ImageUploadingForm
from .services import save_photo_info, save_photo_faces
from .lib.app_logging.custom_logger import CustomLogger


logger = CustomLogger.get_instance()


def delete_file(file_url):
    image_url = build_media_root_path(file_url)
    try:
        os.remove(image_url)
    except Exception:
        logger.error("File [%s] could not be deleted.Exc:\n%s" % (image_url, traceback.format_exc()))
        return False
    else:
        logger.debug("File [%s] has been deleted" % image_url)
        return True


def build_media_root_path(file_url):
    return os.path.join(os.path.dirname(settings.MEDIA_ROOT), file_url[1:])


def build_image_detail_path(img_url):
    filename, extension = os.path.splitext(img_url)
    detail_file = filename + "-detail" + extension
    return detail_file


def handle_file_upload(post, files, user):
    upload_form = ImageUploadingForm(post, files)
    if upload_form.is_valid():
        uploaded_photo = upload_form.save(commit=False)
        uploaded_photo.owner_ref = User.objects.get(username=user)
        upload_form.save()
        img_url = build_media_root_path(uploaded_photo.image.url)
        img_info = _query_image_info(img_url)
        try:
            _save_image_info(uploaded_photo, img_info)
        except:
            logger.warning("Unable to save image info for image: %s. Info: %s" % (uploaded_photo.description, img_info))
        return img_info
    else:
        return None


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
    pi = save_photo_info(photo, photo_info)
    save_photo_faces(pi, photo_info['faces'])


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
            im.save(build_image_detail_path(img_url))
