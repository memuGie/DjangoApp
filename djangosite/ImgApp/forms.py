from django import forms

from .models import Photo


class ImageUploadingForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('description', 'image',)
