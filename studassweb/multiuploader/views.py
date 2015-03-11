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
from base.models import SiteConfiguration

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

        site_config = SiteConfiguration.instance()
        response_data = generate_output(os.path.basename(p.image.path),
                                        p.image.size,
                                        str(site_config.base_url + p.image.url),
                                        str(site_config.base_url + get_thumbnailer(p.image)['standard'].url)
                                        )

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


# Lol remove this when it's confirmed we don't need it.
def jsonize_url(url):
    return url
    result = ''
    for char in url:
        if char == '/':
            result += chr(92)  # That's a \
            result += '/'
        else:
            result += char
    return result


def generate_output(name, size, url, thumbnailurl):
    result = {'files': [
        {"name": name,
         "size": size,
         "url": url,
         "thumbnailUrl": thumbnailurl,
         },
        ]}
    log.info(json.dumps(result))
    return json.dumps(result)
    # "delete_url": reverse('multiuploader_delete', args=[fl.pk]),
    # "delete_type": "POST",


def generate_error_output(error_message):
    return "TODO"
