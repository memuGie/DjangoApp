import json

from django.contrib.auth.models import User

from .models import Photo, PhotoInfo, Face


def get_photo_by_id(photo_id):
    return Photo.objects.get(pk=photo_id)


def get_user_photos_latest_first(user):
    return Photo.objects.filter(
        owner_ref=User.objects.get(username=user)).order_by("upload_date").reverse()


def save_photo_info(photo, photo_info):
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


def save_photo_faces(photo_info, faces_list):
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
