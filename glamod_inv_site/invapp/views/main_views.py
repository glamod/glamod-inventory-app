from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response
from invapp.models import *
import csv
from io import StringIO, BytesIO
import pandas

from ..forms import InventoryForm, ContactForm, UploadContactForm, UploadInventoryForm

# =================================================================
# Contacts
# =================================================================
def upload_contacts( request ):
    if request.method == 'POST' :
        form = UploadContactForm( request.POST, request.FILES )
        if form.is_valid():
            theData = request.FILES['file']
            infile = StringIO( theData.read().decode('utf-8') )
            reader = csv.reader( infile )
            for row in reader:
                contact = Contact( name         = row[0],
                                   organisation = row[1],
                                   emailAddress = row[2],
                                   telephone    = row[3],
                                   address      = row[4],
                                   city         = row[5],
                                   adminArea    = row[6],
                                   postalCode   = row[7],
                                   country      = row[8],
                                   privacy      = True
                )
                contact.save()
            return HttpResponseRedirect('/invapp/contact_all/')
        else :
            return HttpResponse("Error!")
    else :
        form = UploadContactForm()
        return render(request, 'invapp/upload_contacts.html',
                              {'request': request,
                               'form': form})
# ------------------------------------
def edit_contact(request, record_id):
    if request.method == 'POST':
        form = ContactForm( request.POST )
        if form.is_valid() :
            contact = Contact(  **form.cleaned_data )
            contact.pk = record_id
            contact.save()
            return HttpResponseRedirect('/invapp/contact/id={}'.format(contact.pk))
    else :
        contact = Contact.objects.get( pk = record_id )
        form = ContactForm( instance = contact )
        form.helper.form_action = '/invapp/contact/edit/'+str(contact.pk)
        return render(request, 'invapp/input_form.html', {'form': form, 'name': 'Contact', })
# ------------------------------------
def edit_contact_list(request):
    model = Contact
    return render_to_response('invapp/edit_contact_list.html',
                              {'obj': model,
                               'request': request})
# ------------------------------------
def get_contact(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            new_inv = Contact.objects.create(**form.cleaned_data)
            # redirect to a new URL:
            return HttpResponseRedirect('/invapp/contact/{}'.format(new_inv.pk))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()
        return render(request, 'invapp/input_form.html', {'form': form, 'name': 'Contact',})
# ------------------------------------

def view_home(request):
    return render_to_response('invapp/intro.html',
                              {'request': request})


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
    return render_to_response('invapp/record.html',
                              {'record': model.objects.get(pk=record_id),
                               'request': request})


def view_record_all_html(request, record_type):
    record_type_map = {'inventory': Inventory,
                       'contact': Contact}
    model = record_type_map[record_type]
    return render_to_response('invapp/record_all.html',
                              {'obj': model,
                               'request': request})

# =================================================================
# Inventory
# =================================================================
def get_inventory(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InventoryForm(request.POST)
        print('NEW!!!')
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            new_inv = Inventory.objects.create(**form.cleaned_data)
            # redirect to a new URL:
            return HttpResponseRedirect('/invapp/inventory/id={}'.format(new_inv.pk))
        else:
            print('Invalid!!!')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = InventoryForm()

    return render(request, 'invapp/input_form.html', {'form': form, 'name': 'Source', })
# ------------------------------------
def upload_inventory_xls( request ):
    if request.method == 'POST' :
        form = UploadInventoryForm(request.POST, request.FILES)
        if form.is_valid():
            theData = request.FILES['file']
            infile = BytesIO( theData.read() )
            df = pandas.read_excel(  infile  )
            colNames = list(df)
            for row in df.itertuples():
                newinv = Inventory()
                xlsdict = newinv.getDict()
                for key, value in xlsdict.items():
                    colNum = colNames.index( value )
                    if key == 'start_date':
                        val = str(row[colNum+1]) + '-01-01'
                    elif key == 'end_date':
                        val = str(row[colNum + 1]) + '-12-31'
                    else:
                        val = row[colNum + 1]
                    setattr( newinv, key, val )
                newinv.save()
                # add in exception handling, write all bad records to new xls file
            return HttpResponseRedirect('/invapp/inventory_all/')
        else :
            return HttpResponse("Error!")
    else :
        form = UploadInventoryForm()
        return render(request, 'invapp/upload_inventory_xls.html',
                              {'request': request,
                               'form': form})
# ------------------------------------
def edit_inventory(request, record_id):
    if request.method == 'POST':
        form = InventoryForm( request.POST )
        if form.is_valid() :
            inventory = Inventory(  **form.cleaned_data )
            inventory.pk = record_id
            inventory.save()
            return HttpResponseRedirect('/invapp/inventory/id={}'.format(inventory.pk))
    else :
        inventory = Inventory.objects.get( pk = record_id )
        form = InventoryForm( instance = inventory )
        form.helper.form_action = '/invapp/inventory/edit/'+str(inventory.pk)
        return render(request, 'invapp/input_form.html', {'form': form, 'name': 'Inventory', })

# ------------------------------------
def edit_inventory_list(request):
    model = Inventory
    return render_to_response('invapp/edit_inventory_list.html',
                              {'obj': model,
                               'request': request})