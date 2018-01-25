import tempfile

from django.test import TestCase
from django.utils import timezone

from ..services import *


class ServicesTest(TestCase):

    def setUp(self):
        self._user = User.objects.create_user(
            username="servicesTest", email="service@mm.ww", password=""
        )
        self._photo1 = Photo.objects.create(
            description="test photo 1",
            upload_date=timezone.now(),
            owner_ref=self._user,
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )
        self._photo2 = Photo.objects.create(
            description="test photo 2",
            upload_date=timezone.now(),
            owner_ref=self._user,
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )

    def test_get_photo_by_id(self):
        self.assertEqual(get_photo_by_id(1), self._photo1)
        self.assertEqual(get_photo_by_id(2), self._photo2)

    def test_get_user_photos_latest_first(self):
        self.assertEqual(get_user_photos_latest_first(self._user)[0], self._photo2)
        self.assertEqual(get_user_photos_latest_first(self._user)[1], self._photo1)
