from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.shortcuts import render_to_response
from invapp.models import *

from ..forms import InventoryForm


def view_intro(request):
    return render_to_response('invapp/intro.html', 
                              {'request': request})


def view_source_level_inventory(request):
    return render_to_response('invapp/full_inventory.html',
                              {'records': Inventory.objects.all(),
                               'request': request})


def view_record_html(request, record_type, record_id):
    record_type_map = {'inventory': Inventory,
                       'contact': Contact}
    model = record_type_map[record_type]

    return render_to_response('invapp/inventory_record.html',
                              {'record': model.objects.get(pk=record_id),
                               'request': request})


def get_inventory(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InventoryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = InventoryForm()

    return render(request, 'invapp/inventory_form.html', {'form': form})
