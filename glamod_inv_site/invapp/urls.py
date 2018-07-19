from django.conf.urls import include, url
import invapp.views.xml_views
import invapp.views.main_views

urlpatterns = [

    url(r'^inventories/source-level', invapp.views.main_views.view_source_level_inventory), 
    url(r'^inventory/add/$', invapp.views.main_views.get_inventory, name='add-record'),
    url(r'^inventory/upload/$', invapp.views.main_views.upload_inventory_xls, name='upload-inventory'),
    url(r'^inventory/edit/(?P<record_id>.+)/?$', invapp.views.main_views.edit_inventory, name='edit-inventory'),
    url(r'^inventory/edit/', invapp.views.main_views.edit_inventory_list, name='edit-inventory-list'),
    url(r'^contact/add/$', invapp.views.main_views.get_contact, name='add-contact'),
    url(r'^contact/upload/$', invapp.views.main_views.upload_contacts, name='upload-contacts'),
    url(r'^contact/edit/(?P<record_id>.+)/?$', invapp.views.main_views.edit_contact, name='edit-contact'),
    url(r'^contact/edit/', invapp.views.main_views.edit_contact_list, name='edit-contact-list'),
    url(r'^export/xml/(?P<record_id>.+)\.xml$', invapp.views.xml_views.view_gemini_xml),
    url(r'^intro', invapp.views.main_views.view_intro),
    url(r'^home', invapp.views.main_views.view_home),
    url(r'^(?P<record_type>.+)/id=(?P<record_id>.+)/?$', invapp.views.main_views.view_record_html, name='record-view'),
    url(r'^(?P<record_type>.+)_all/', invapp.views.main_views.view_record_all_html, name='record-view-all'),
    url(r'^(?P<record_type>.+)/', invapp.views.main_views.view_record_all_html, name='record-view-all'),
    url(r'.*', invapp.views.main_views.view_home),
    url(r'^tinymce/', include('tinymce.urls')),
]
