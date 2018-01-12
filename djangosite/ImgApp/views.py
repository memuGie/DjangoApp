from .app_logging.custom_logger import CustomLogger

from django.shortcuts import render

from django.http import HttpResponse

#TODO: fix Django logging in order not to use the CustomLogger -> settings.py
logger = CustomLogger.get_instance()


def index(request):
    if not request.user.is_authenticated:
        return HttpResponse("""Please <a href="login">login</a>...""")
    logger.info("User %s has logged in" % request.user)
    return render(request, "ImgApp/index.html")

