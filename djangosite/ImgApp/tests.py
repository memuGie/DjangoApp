from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import AnonymousUser, User

from .views import index
from .models import Photo


class StatusTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="Mick", email="mickey@m0ck.com", password="")

    def test_index_anonymous(self):
        request = self.factory.get('/index')
        request.user = AnonymousUser()

        resp = index(request)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue("login".encode() in resp.content)

    def test_index_user(self):
        request = self.factory.get('/index')
        request.user = self.user

        resp = index(request)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue("Proud html index page!".encode() in resp.content)
