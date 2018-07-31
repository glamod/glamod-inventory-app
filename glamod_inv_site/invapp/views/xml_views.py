
from django.shortcuts import render_to_response


def view_gemini_xml_old(request, record_id):
    dct = {'ob_id': record_id} 

    return render_to_response("invapp/xml/gemini.xml", dct,
                              content_type = "text/xml;")
