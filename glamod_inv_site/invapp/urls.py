from django.conf.urls import include, url
import invapp.views.xml_views
import invapp.views.main_views

urlpatterns = [

    url(r'^inventories/source-level', invapp.views.main_views.view_source_level_inventory), 
    url(r'^record/(?P<record_id>.+)/?$', invapp.views.main_views.view_record_html),
    url(r'^add/$', invapp.views.main_views.get_inventory),
    url(r'^export/xml/(?P<record_id>.+)\.xml$', invapp.views.xml_views.view_gemini_xml),
    url(r'^intro', invapp.views.main_views.view_intro)
]
