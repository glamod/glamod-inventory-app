from django.conf.urls import include, url
import invapp.views.xml_views
import invapp.views.main_views

urlpatterns = [

    url(r'^inventories/source-level', invapp.views.main_views.view_source_level_inventory), 
    url(r'^inventory/add/$', invapp.views.main_views.get_inventory, name='add-record'),
    url(r'^export/xml/(?P<record_id>.+)\.xml$', invapp.views.xml_views.view_gemini_xml),
    url(r'^intro', invapp.views.main_views.view_intro),
    url(r'^home', invapp.views.main_views.view_home),
    url(r'^(?P<record_type>.+)/(?P<record_id>.+)/?$', invapp.views.main_views.view_record_html, name='record-view'),
    url(r'.*', invapp.views.main_views.view_home),
]
