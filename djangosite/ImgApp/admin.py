from django.contrib import admin

from .models import Photo, PhotoInfo, Face

admin.site.register(Photo)
admin.site.register(PhotoInfo)
admin.site.register(Face)
