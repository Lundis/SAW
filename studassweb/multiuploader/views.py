import logging


from django.conf import settings

try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.core.signing import Signer, BadSignature
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
import os

from .utils import FileResponse
from .models import MultiuploaderFile
from .forms import MultiUploadForm, MultiuploaderMultiDeleteForm

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


def multiuploader_delete(request, pk):
    if request.method == 'POST':
        log.info('Called delete file. File id=' + str(pk))
        fl = get_object_or_404(MultiuploaderFile, pk=pk)
        fl.delete()
        log.info('DONE. Deleted file id=' + str(pk))

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
        #print(request.POST)

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

        # Remove this, we use csrf + unique_id
        #signer = Signer()
        """
        try:
            form_type = signer.unsign(request.POST.get(u"form_type"))
        except BadSignature:
            response_data = [{"error": _("Tampering detected!")}]
            return HttpResponse(json.dumps(response_data))
        """

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
        file = request.FILES[u'file']
        wrapped_file = UploadedFile(file)
        # TODO don't take extension from uploaded file, it should be hardcoded jpg/png/gif etc
        filename = unique_id + '.' + wrapped_file.name.split('.')[-1]
        file_size = wrapped_file.file.size
        upload_to_folder = os.path.join(settings.MEDIA_ROOT, "gallery") # TODO

        log.info('Got file: "%s"' % filename)

        #writing file manually into model
        #because we don't need form of any type.

        #fl = MultiuploaderFile()
        #fl.filename = filename
        #fl.file = file
        #fl.save()

        # make dir if not exists already
        if not os.path.exists(upload_to_folder):
            os.makedirs(upload_to_folder)

        filename = os.path.join(upload_to_folder, filename)
        # open the file handler with write binary mode
        destination = open(filename, "wb+")
        # save file data into the disk
        # use the chunk method in case the file is too big
        # in order not to clutter the system memory
        for chunk in file.chunks():
            destination.write(chunk)
        # close the file
        destination.close()


        log.info('File saving done')

        thumb_url = ""

        #try:
        #    im = get_thumbnail(fl.file, "80x80", quality=50)
        #    thumb_url = im.url
        #except Exception as e:
        #    log.error(e)

        #generating json response array
        result = [{#"id": fl.id,
                   "name": filename,
                   "size": file_size,
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
