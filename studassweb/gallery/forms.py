from django import forms
from gallery.models import *
from datetime import date


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ('author', 'description', 'name')


class PictureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PictureForm, self).__init__(*args, **kwargs)
        self.fields['album_id'].label_from_instance = lambda obj: "%s" % obj.name

    uploaded = forms.DateTimeField(
        widget=forms.DateInput(format='%d.%m.%Y'),
        input_formats=('%d.%m.%Y',),
        initial=date.today)

    class Meta:
        model = Photo
        fields = ('album_id', 'author', 'description', 'uploaded')
