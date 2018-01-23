from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User

from ..views import index


class StatusTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self._user = User.objects.create_user(
            username="Mick", email="mickey@m0ck.com", password="")

    def test_index_anonymous(self):
        request = self.factory.get('/index')
        request.user = AnonymousUser()

        resp = index(request)

        self.assertEqual(resp.status_code, 302)

    def test_index_user(self):
        request = self.factory.get('/index')
        request.user = self._user

        resp = index(request)

        self.assertEqual(resp.status_code, 200)
