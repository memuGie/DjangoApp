from django.test import TestCase
from django.conf import settings

from ..view_functions import *


class ViewFunctionsTest(TestCase):

    def setUp(self):
        pass

    def test_build_image_detail_path(self):
        url = "my/test/image/photo.jpg"
        self.assertEqual(build_image_detail_path(url), "my/test/image/photo-detail.jpg")

    def test_build_media_root_path(self):
        filename = "/myfile.jpg"
        self.assertEqual(build_media_root_path(filename),
                         os.path.join(os.path.dirname(settings.MEDIA_ROOT), filename[1:]))

    def test_delete_file(self):
        filename = "/sample_file.txt"
        f = open(build_media_root_path(filename), 'wb')
        f.close()
        self.assertTrue(delete_file(filename))
        self.assertFalse(delete_file(filename))

    def test_handle_file_upload(self):
        pass

    def test_query_image_info(self):
        # access the protected method
        # self.assertIsNone(_query_image_info("noimage.pong"), )
        pass
