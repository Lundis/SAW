from django import forms
from gallery.models import *
from datetime import date
from multiuploader.forms import MultiuploaderField


class AlbumForm(forms.ModelForm):
    uploadedFiles = MultiuploaderField(required=False)

    class Meta:
        model = Album
        fields = ('description', 'name')

    def save(self, user, commit=True,):
        temp_album = super().save(commit=False)
        if not user.is_anonymous():
            temp_album.user = user
        if commit:
            temp_album.save()
        return temp_album


class PictureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['album'].label_from_instance = lambda obj: "%s" % obj.name

    uploaded = forms.DateTimeField(
        widget=forms.DateInput(format='%d.%m.%Y'),
        input_formats=('%d.%m.%Y',),
        initial=date.today)

    class Meta:
        model = Photo
        fields = ('album', 'description', 'uploaded')

    def save(self, user, commit=True,):
        temp_photo = super().save(commit=False)
        if not user.is_anonymous():
            temp_photo.user = user
        if commit:
            temp_photo.save()
        return temp_photo
