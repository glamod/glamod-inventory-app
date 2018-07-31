from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response
from invapp.models import *


import csv
from io import StringIO, BytesIO
import pandas

from ..forms import InventoryForm, ContactForm, UploadContactForm, UploadInventoryForm
from ..forms import InventoryHistoryForm, GeminiValidate

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
            return HttpResponseRedirect('/invapp/contact/{}'.format(contact.pk))
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
def add_contact(request):
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
# ====================================
# Generic record views
# ====================================
# View single record
# ------------------
def view_record_html(request, record_type, record_id):
    record_type_map = {'inventory': Inventory,
                       'contact': Contact,
                       'role': Role}
    model = record_type_map[record_type]
    if record_type == 'inventory':
        # get histories associated with this ID
        links = LinkInvHist.objects.filter( inventory = record_id ).order_by('history__date')
        dct = {
            'record': model.objects.get(pk=record_id),
            'request': request,
            'history': links
        }
    else:
        dct = {'record': model.objects.get(pk=record_id),
                               'request': request}

    return render_to_response('invapp/record.html',
                              dct )
# -------------------
# View all records
# -------------------
def view_record_all_html(request, record_type):
    record_type_map = {'inventory': Inventory,
                       'contact': Contact,
                       'role': Role,
                       'update_frequency': UpdateFrequency,
                       'geometry_type': GeometryType}

    model = record_type_map[record_type]
    return render_to_response('invapp/record_all.html',
                              {'obj': model,
                               'request': request})
# ====================================
# Other pages / views
# ====================================
def view_home(request):
    print( 'home' )
    return render_to_response('invapp/intro.html',
                              {'request': request})
# -----------
def view_intro(request):
    print( 'intro' )
    return render_to_response('invapp/intro.html', 
                              {'request': request})
# -----------

#def view_source_level_inventory(request):
#    return render_to_response('invapp/full_inventory.html',
#                              {'records': Inventory.objects.all(),
#                               'request': request})




# =================================================================
# Inventory
# =================================================================
# Form to bulk upload inventory from xls file
# -------------------------------------------
# TODO - add in history
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
        form = UploadInventoryForm()
    return render(request, 'invapp/upload_inventory_xls.html',
                              {'request': request,
                               'form': form})
# -------------------------------------------
# Form to create new record
# -------------------------------------------
def add_inventory(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        invForm  = InventoryForm(request.POST, prefix='inv')
        histForm = InventoryHistoryForm(request.POST, prefix='hist')
        if all( {invForm.is_valid() , histForm.is_valid() }):
            histForm.cleaned_data['action'] = 'create'
            invModel  = Inventory.objects.create(**invForm.cleaned_data)
            histModel = InventoryHistory.objects.create(**histForm.cleaned_data)
            linkModel = LinkInvHist.objects.create( inventory = invModel, history = histModel  )
            return HttpResponseRedirect('/invapp/inventory/{}'.format(invModel.pk))
        else:
            print('invalid')

    # if a GET (or any other method) we'll create a blank form
    else:
        # init forms
        invForm = InventoryForm(prefix='inv')
        histForm = InventoryHistoryForm(prefix='hist')
    return render(request, 'invapp/inventory_form.html', {'inventory': invForm, 'history': histForm, 'name': 'Source', })
# -------------------------------------------
# Form to edit inventory record
# -------------------------------------------
def edit_inventory(request, record_id):
    if request.method == 'POST':
        invForm  = InventoryForm(request.POST, prefix='inv')
        histForm = InventoryHistoryForm(request.POST, prefix='hist')
        try:
            invForm.full_clean()
            histForm.full_clean()
            invModel = Inventory(**invForm.cleaned_data)
            invModel.pk = record_id
            invModel.save()
            histForm.cleaned_data['action'] = 'update'
            histModel = InventoryHistory.objects.create( **histForm.cleaned_data )
            linkModel = LinkInvHist.objects.create(inventory=invModel, history=histModel)
            return HttpResponseRedirect('/invapp/inventory/{}'.format(invModel.pk))
        except:
            raise forms.ValidationError('Invalid form')
    else :
        inventory = Inventory.objects.get( pk = record_id )
        invForm = InventoryForm( instance = inventory , prefix = 'inv' )
        histForm = InventoryHistoryForm(prefix='hist', initial={'description':''})
    return render(request, 'invapp/inventory_form.html', {'inventory': invForm, 'history': histForm, 'name': 'Source', 'id': str(inventory.pk) })
# ------------------------------------
# Form to list entries
# ------------------------------------
def edit_inventory_list(request):
    model = Inventory
    return render_to_response('invapp/edit_inventory_list.html',
                              {'obj': model,
                               'request': request})
# -------------------------------------
# view to export to iso19139 xml format
# -------------------------------------
def view_gemini_xml( request , record_id ):
    inventory = Inventory.objects.get( pk = record_id )
    meta_contact = Inventory.objects.select_related('contact_metadata').get( pk = record_id )
    data_contact = Inventory.objects.select_related('contact_data').get( pk = record_id )
    dct = { 'source': inventory, 'meta_contact': meta_contact.contact_metadata, 'data_contact': data_contact.contact_data }
    r = render(request,"invapp/xml/gemini.xml", dct, content_type="text/xml;")
    print (r.content )
    #return HttpResponseRedirect('http://www.google.com')
    return r # render(request,"invapp/xml/gemini.xml", dct, content_type="text/xml;")



def validate_gemini_xml( request, record_id ):
    inventory = Inventory.objects.get(pk=record_id)
    meta_contact = Inventory.objects.select_related('contact_metadata').get(pk=record_id)
    data_contact = Inventory.objects.select_related('contact_data').get(pk=record_id)
    dct = {'source': inventory, 'meta_contact': meta_contact.contact_metadata,
           'data_contact': data_contact.contact_data}
    r = render(request, "invapp/xml/gemini.xml", dct, content_type="text/xml;")

    form = GeminiValidate(initial={'input': str(r.content,'utf-8') })

    return render(request, 'invapp/gemini_validate.html',
                  {'form': form})

# =================================================================
#def get_inventory(request):
#    # if this is a POST request we need to process the form data
#    if request.method == 'POST':
#        # create a form instance and populate it with data from the request:
#        form = InventoryForm(request.POST)
#        # check whether it's valid:
#        if form.is_valid():
#            # process the data in form.cleaned_data as required
#            new_inv = Inventory.objects.create(**form.cleaned_data)
#            # redirect to a new URL:
#            return HttpResponseRedirect('/invapp/inventory/id={}'.format(new_inv.pk))
#    # if a GET (or any other method) we'll create a blank form
#    else:
#        form = InventoryForm()
#    return render(request, 'invapp/input_form.html', {'form': form, 'name': 'Source', })
# ------------------------------------
#def edit_inventory(request, record_id):
#    if request.method == 'POST':
#        form = InventoryForm( request.POST )
#        try:
#            form.full_clean( )
#            inventory = Inventory(**form.cleaned_data)
#            inventory.pk = record_id
#            inventory.save()
#            return HttpResponseRedirect('/invapp/inventory/id={}'.format(inventory.pk))
#        except:
#            raise forms.ValidationError('Invalid form')
#    else :
#        inventory = Inventory.objects.get( pk = record_id )
#        inventory.history = 'Update'
#        form = InventoryForm( instance = inventory )
#        form.helper.form_action = '/invapp/inventory/edit/'+str(inventory.pk)
#    return render(request, 'invapp/input_form.html', {'form': form, 'name': 'Inventory', })
# =================================================================