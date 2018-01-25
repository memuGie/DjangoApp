import tempfile

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from ..models import Photo, PhotoInfo, Face


class ModelTests(TestCase):
    def setUp(self):
        self._user = User.objects.create_user(
            username="Mick", email="mickey.mock@mm.ww", password=""
        )
        self._photo = Photo.objects.create(
            description="test photo from Mallorca",
            upload_date=timezone.now(),
            owner_ref=self._user,
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )
        self._photo_info = PhotoInfo.objects.create(
            caption="a photo taken on Mallorca",
            tags="['mallorca', 'people', 'posing', 'couple']",
            raw_json="{'test': 'test value'}",
            width=500,
            height=500,
            format="jpg",
            photo_ref=self._photo
        )
        self._face1 = Face.objects.create(
            age=30,
            gender="Male",
            top=30,
            left=30,
            width=50,
            height=50,
            photo_info_ref=self._photo_info
        )
        self._face2 = Face.objects.create(
            age=25,
            gender="Female",
            top=30,
            left=70,
            width=50,
            height=50,
            photo_info_ref=self._photo_info
        )
        self._photo.save()

    def test_photo_attributes(self):
        self.assertEqual(self._photo.description, "test photo from Mallorca")
        self.assertEqual(self._photo.owner_ref, self._user)
        self.assertTrue(self._photo.image.url)

    def test_photo_photo_info(self):
        self.assertEqual(self._photo.photoinfo, self._photo_info)

    def test_photo_info_attributes(self):
        self.assertEqual(self._photo_info.caption, "a photo taken on Mallorca")
        self.assertEqual(self._photo_info.tags, "['mallorca', 'people', 'posing', 'couple']")
        self.assertEqual(self._photo_info.raw_json, "{'test': 'test value'}")
        self.assertEqual(self._photo_info.width, 500)
        self.assertEqual(self._photo_info.height, 500)
        self.assertEqual(self._photo_info.format, "jpg")
        self.assertEqual(self._photo_info.photo_ref, self._photo)

    def test_photo_info_faces(self):
        self.assertEqual(self._photo_info.face_set.get(pk=1), self._face1)
        self.assertEqual(self._photo_info.face_set.get(pk=2), self._face2)

    def test_face_attributes(self):
        self.assertEqual(self._face1.age, 30)
        self.assertEqual(self._face1.gender, "Male")
        self.assertEqual(self._face1.top, 30)
        self.assertEqual(self._face1.left, 30)
        self.assertEqual(self._face1.width, 50)
        self.assertEqual(self._face1.height, 50)
        self.assertEqual(self._face1.photo_info_ref, self._photo_info)
