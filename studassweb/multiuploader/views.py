import logging


from django.conf import settings

try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse, HttpResponseBadRequest
import os

from .utils import FileResponse
from .forms import MultiUploadForm, MultiuploaderMultiDeleteForm

# TODO move this later
from gallery.models import Album, Photo

# TODO change to the other thumbnail lib
# from sorl.thumbnail import get_thumbnail

log = logging.getLogger(__name__)


def multiuploader_delete_multiple(request, ok=False):
    if request.method == 'POST':

        form = MultiuploaderMultiDeleteForm(request.POST)

        if form.is_valid():
            return redirect(request.META.get('HTTP_REFERER', None))
        else:
            pass

        """fl = get_object_or_404(MultiuploaderFile, pk=pk)
        fl.delete()
        log.info('DONE. Deleted file id=' + str(pk))"""

        return HttpResponse(1)

    else:
        log.info('Received not POST request to delete file view')
        return HttpResponseBadRequest('Only POST accepted')


def multiuploader(request, noajax=False):
    """
    Main Multiuploader module.
    Parses data from jQuery plugin and makes database changes.
    """

    if request.method == 'POST':
        log.info('received POST to main multiuploader view')

        log.debug('Checking request.FILES')
        if request.FILES is None:
            log.error('No files attached')
            response_data = [{"error": _('Must have files attached!')}]
            return HttpResponse(json.dumps(response_data))

        log.debug('Checking form_type')
        if not u'form_type' in request.POST:
            log.error('Form type is missing')
            response_data = [{"error": _("Error when detecting form type, form_type is missing")}]
            return HttpResponse(json.dumps(response_data))

        # We get one request for each file, this id connects them.
        log.debug('Checking unique id')
        if not request.POST[u"unique_id"]:
            log.error('Unique id is missing')
            response_data = [{"error": _("unique_id is missing")}]
            return HttpResponse(json.dumps(response_data))
        unique_id = request.POST[u"unique_id"]

        if not request.POST[u"album_pk"]:
            log.error('album_pk is missing')
            response_data = [{"error": _("album_pk is missing")}]
            return HttpResponse(json.dumps(response_data))
        album_pk = request.POST[u"album_pk"]

        try:
            album = Album.objects.get(slug=album_pk)
        except Album.DoesNotExist:
            log.error('Tried to add photos with wrong album_pk: {0}'.format(album_pk))
            response_data = [{"error": _("album_pk is wrong!")}]
            return HttpResponse(json.dumps(response_data))

        form_type = request.POST.get(u"form_type")
        form = MultiUploadForm(request.POST, request.FILES, form_type=form_type)

        log.debug('Check if form is valid')
        if not form.is_valid():
            log.warning('Form is not valid')
            log.warning(form._errors)
            error = _("Unknown error")

            if "file" in form._errors and len(form._errors["file"]) > 0:
                error = form._errors["file"][0]

            response_data = [{"error": error}]
            return HttpResponse(json.dumps(response_data))

        log.debug('Get the file')

        log.info('saving in a Photo()')
        # Writing it into model:
        # TODO this should somehow be set somewhere else
        p = Photo()
        p.image = request.FILES[u'file']
        p.album = album
        p.save()


        thumb_url = ""

        #try:
        #    im = get_thumbnail(fl.file, "80x80", quality=50)
        #    thumb_url = im.url
        #except Exception as e:
        #    log.error(e)

        #generating json response array
        result = [{"id": p.id,
                   #"name": filename,
                   #"size": file_size,
                   #"url": reverse('multiuploader_file_link', args=[fl.pk]),
                   #"thumbnail_url": thumb_url,
                  # "delete_url": reverse('multiuploader_delete', args=[fl.pk]),
                  # "delete_type": "POST",
                  }]

        response_data = json.dumps(result)

        #checking for json data type
        #big thanks to Guy Shapiro

        if noajax:
            if request.META['HTTP_REFERER']:
                redirect(request.META['HTTP_REFERER'])

        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, content_type="{0}; charset=utf-8".format(mimetype))
    else:  # GET
        return HttpResponse('Only POST accepted')


def multi_show_uploaded(request, pk):
    fl = get_object_or_404(MultiuploaderFile, id=pk)
    return FileResponse(request,fl.file.path, fl.filename)
