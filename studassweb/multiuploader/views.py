import logging

try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.http import HttpResponse
import os

from .forms import MultiUploadForm

# TODO move this later
from gallery.models import Album, Photo

from easy_thumbnails.files import get_thumbnailer

log = logging.getLogger(__name__)


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
            return json_response(generate_output(error=_('Must have files attached!')), request)

        log.debug('Checking form_type')
        if u'form_type' not in request.POST:
            log.error('Form type is missing')
            return json_response(generate_output(error=_('Error when detecting form type, form_type is missing')), request)

        # We get one request for each file, this id connects them.
        # Obsolete? As for now we only care about which album to put the file in
        log.debug('Checking unique id')
        if not request.POST[u"unique_id"]:
            log.error('Unique id is missing')
            return json_response(generate_output(error=_('unique_id is missing')), request)
        unique_id = request.POST[u"unique_id"]

        if not request.POST[u"album_pk"]:
            log.error('album_pk is missing')
            return json_response(generate_output(error=_('album_pk is missing')), request)
        album_pk = request.POST[u"album_pk"]

        try:
            album = Album.objects.get(slug=album_pk)
        except Album.DoesNotExist:
            log.error('Tried to add photos with wrong album_pk: {0}'.format(album_pk))
            return json_response(generate_output(error=_('album_pk is wrong')), request)

        form_type = request.POST.get(u"form_type")
        form = MultiUploadForm(request.POST, request.FILES, form_type=form_type)

        log.debug('Check if form is valid')
        if not form.is_valid():
            log.warning('Form is not valid')
            log.warning(form._errors)
            error = _("Unknown error")

            if "file" in form._errors and len(form._errors["file"]) > 0:
                error = form._errors["file"][0]

            try:
                name = form.files['file'][0]._name
                size = str(form.files['file'][0]._size)
            except:
                name = ""
                size = ""
            return json_response(generate_output(name=name, size=size, error=error), request)

        log.debug('Get the file')

        log.info('saving in a Photo()')
        # Writing it into model:
        # TODO this should somehow be set somewhere else
        p = Photo()
        p.image = request.FILES[u'file']
        p.album = album
        p.save()

        response_data = generate_output(name=os.path.basename(p.image.path),
                                        size=p.image.size,
                                        url=str(p.image.url),
                                        thumbnailurl=str(get_thumbnailer(p.image)['standard'].url)
                                        )
        return json_response(response_data, request)

    else:  # GET
        return HttpResponse('Only POST accepted')


def generate_output(name=None, size=None, url=None, thumbnailurl=None, error=None):
    status_list = {}
    if name is not None:
        status_list["name"] = name
    if size is not None:
        status_list["size"] = size
    if url is not None:
        status_list["url"] = url
    if thumbnailurl is not None:
        status_list["thumbnailUrl"] = thumbnailurl
    if error is not None:
        status_list["error"] = error

    result = {'files': [status_list]}
    log.info(json.dumps(result))
    return json.dumps(result)
    # "delete_url": reverse('multiuploader_delete', args=[fl.pk]),
    # "delete_type": "POST",


def json_response(response_data, request, noajax=False):
    # checking for json data type
    # big thanks to Guy Shapiro

    if noajax:
        if request.META['HTTP_REFERER']:
            redirect(request.META['HTTP_REFERER'])

    if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
        mimetype = 'application/json'
    else:
        mimetype = 'text/plain'
    return HttpResponse(response_data, content_type="{0}; charset=utf-8".format(mimetype))