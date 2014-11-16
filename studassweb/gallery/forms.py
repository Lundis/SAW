from django import forms
from gallery.models import *

class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ('author', 'created','description', 'modified', 'name')


class PictureForm(forms.Form):

    class Meta:
        model = Photo
        fields = ('album_id', 'author', 'description', 'image','uploaded')