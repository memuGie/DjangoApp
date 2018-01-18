# source: https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts/python

import requests

from .app_logging.custom_logger import CustomLogger

logger = CustomLogger.get_instance()

headers = {
    # Request headers.
    'Content-Type': 'application/octet-stream',

    # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
    'Ocp-Apim-Subscription-Key': 'b01e8bfda2cd428f9f1350b73b920945',
}

params = {
    # Request parameters. All of them are optional.
    # more:
    #  https://westus.dev.cognitive.microsoft.com/docs/services/56f91f2d778daf23d8ec6739/operations/56f91f2e778daf14a499e1fa
    'visualFeatures': 'Categories,Description,Color,Faces',
    'details': 'Celebrities',
    'language': 'en',
}


def get_image_info(image_url):
    import json

    try:
        image = open("%s" % image_url, 'rb').read()  # Read image file in binary mode
        # NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
        #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the
        #   URL below with "westus".
        response = requests.post(url='https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/analyze',
                                 headers=headers,
                                 params=params,
                                 data=image)
        data = response.json()
        logger.debug(data)
        return json.dumps(data)
    except:
        import traceback
        logger.exception("Exception occured:\n%s" % traceback.format_exc())
