import tempfile

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from ..models import Photo


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

    def test_create_photo(self):
        self.assertEqual(self._photo.description, "test photo from Mallorca")
        self.assertEqual(self._photo.owner_ref, self._user)
        self.assertTrue(self._photo.image.url)
