from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ConfirmationForm


def delete_confirmation_view(request, item, form_url, redirect_url):
    form = ConfirmationForm(request.POST or None)
    item_name = str(item)
    if form.is_valid():
        item.delete()
        if redirect_url:
            return HttpResponseRedirect(redirect_url)
        else:
            form = None
    context = {'form': form,
               'item': item,
               'form_url': form_url,
               'item_name': item_name}
    return render(request, "base/delete_confirmation.html", context)