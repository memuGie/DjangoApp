from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    if not request.user.is_authenticated:
        return HttpResponse("""Please <a href="login">login</a>...""")
    return render(request, "ImgApp/index.html")

