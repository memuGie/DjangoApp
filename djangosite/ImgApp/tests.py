import tempfile

from django.utils import timezone
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User

from .views import index
from .models import Photo


class StatusTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self._user = User.objects.create_user(
            username="Mick", email="mickey@m0ck.com", password="")

    def test_index_anonymous(self):
        request = self.factory.get('/index')
        request.user = AnonymousUser()

        resp = index(request)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue("login".encode() in resp.content)

    def test_index_user(self):
        request = self.factory.get('/index')
        request.user = self._user

        resp = index(request)

        self.assertEqual(resp.status_code, 200)


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
