import tempfile

from django.test import Client
from django.urls import reverse
from django.utils import timezone
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User

from ..views import index
from ..models import Photo


class StatusTest(TestCase):

    def setUp(self):
        self._client = Client()
        self.factory = RequestFactory()
        self._user = User.objects.create_user(
            username="Mick", email="mickey@m0ck.com", password="")
        self._index_request = self.factory.get('/index')

    def test_index_anonymous(self):
        self._index_request.user = AnonymousUser()
        resp = index(self._index_request)
        self.assertEqual(resp.status_code, 302)

    def test_index_user(self):
        self._index_request.user = self._user
        resp = index(self._index_request)
        self.assertEqual(resp.status_code, 200)

    def test_index_no_user_photos(self):
        self._index_request.user = self._user
        resp = index(self._index_request)
        self.assertContains(resp, "You don't have any pictures. Upload something...")

    def test_index_with_user_photos(self):
        p = Photo.objects.create(
            description="test photo",
            upload_date=timezone.now(),
            owner_ref=self._user,
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )
        self._client.login(username="Mick", password="")
        resp = self._client.get(reverse("imgapp:index"))
        self.assertQuerysetEqual(resp.context['user_photos'], ['<Photo: Photo object (1)>'])

    def test_photo_detail_view(self):
        pass
