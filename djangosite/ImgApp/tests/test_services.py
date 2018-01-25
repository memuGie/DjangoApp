import os
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
        cur_path = os.path.dirname(__file__)
        self._json_content = json.loads(open(os.path.join(cur_path, "test.json"), 'r').read())

    def test_get_photo_by_id(self):
        self.assertEqual(get_photo_by_id(1), self._photo1)
        self.assertEqual(get_photo_by_id(2), self._photo2)

    def test_get_user_photos_latest_first(self):
        self.assertEqual(get_user_photos_latest_first(self._user)[0], self._photo2)
        self.assertEqual(get_user_photos_latest_first(self._user)[1], self._photo1)

    def test_save_photo_info(self):
        pi = save_photo_info(self._photo1, self._json_content)
        self.assertEqual(pi.caption, "a person posing for the camera")
        self.assertIn("wooden", pi.tags)
        self.assertEqual(pi.raw_json, json.dumps(self._json_content))

    def test_save_photo_faces(self):
        pi = save_photo_info(self._photo1, self._json_content)
        save_photo_faces(pi, self._json_content['faces'])
        face1 = pi.face_set.get(pk=1)
        face2 = pi.face_set.get(pk=2)
        self.assertEqual(face1.age, 45)
        self.assertEqual(face1.gender, "Male")
        self.assertEqual(face1.left, 553)
        self.assertEqual(face1.top, 178)
        self.assertEqual(face1.width, 273)
        self.assertEqual(face1.height, 273)
        self.assertEqual(face2.age, 30)
        self.assertEqual(face2.gender, "Female")
        self.assertEqual(face2.left, 299)
        self.assertEqual(face2.top, 261)
        self.assertEqual(face2.width, 253)
        self.assertEqual(face2.height, 253)
