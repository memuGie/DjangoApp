import tempfile
from unittest.mock import MagicMock

from django.utils import timezone
from django.test import TestCase, RequestFactory, Client
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
        self.assertTrue("Proud html index page!".encode() in resp.content)


class ModelTests(TestCase):
    def setUp(self):
        self._user = User.objects.create_user(
            username="Mick", email="mickey.mock@mm.ww", password=""
        )
        self._photo = Photo.objects.create(
            name="test photo from Mallorca",
            upload_date=timezone.now(),
            owner_ref=self._user,
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )

    def test_create_photo(self):
        pass
