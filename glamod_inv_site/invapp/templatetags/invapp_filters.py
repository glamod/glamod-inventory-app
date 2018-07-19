import stringcase

from django import template
register = template.Library()

from django.contrib.gis.db import models
from invapp.models import *


# Set limit on number of objects to show
_LIMIT = 20

def _get_obj_link(obj, app_label):
    cls_name = obj.__class__.__name__.split(".")[-1]
    slug_name = stringcase.snakecase(cls_name)
    return '/{}/{}/{}'.format(app_label, slug_name, obj.pk)


def _titlecamelcase(s):
    return s[0].upper() + stringcase.camelcase(s)[1:]


def _get_obj_links_list(field_name, pk_list, app_label):
    resp = []
    cls = _titlecamelcase(field_name)
    try:
        mod = eval(cls)
    except:
        mod = None

    for pk in pk_list:
        tooltip = 'No info provided'
        url = None

        if mod:
            tooltip = mod.objects.get(pk=pk)
            url = '/{}/{}s/{}/'.format(app_label, field_name, pk)

        resp.append((pk, url, tooltip))

    return resp


def _get_reverse_fk_set(obj, field_name):
    # Set default display name
    display_name = field_name
    lookup = '{}_set'.format(field_name)
    
    print('[INFO] RFK lookup count: {}'.format(getattr(obj, lookup).count()))
    obj_set = getattr(obj, lookup).all()

    pk_url_list = []

    try:
        for robj in obj_set[:_LIMIT]:
            if robj == obj_set.first():
                display_name = robj._meta.label.split('.')[-1]

            tooltip = robj
            url = _get_obj_link(robj, robj._meta.app_label)
            pk = robj.pk
            pk_url_list.append((pk, url, tooltip))        
    except:
        pk_url_list.append(('CANNOT RESOLVE THE REFERENCES FOR THIS PROPERTY!!!', None, None))
         
    return 'Related {}s'.format(display_name), {'pk_url_list': pk_url_list}



@register.filter
def get_field_names(obj):
    field_names = [field.name for field in obj._meta.get_fields()]
    return field_names

@register.filter
def get_all(obj):
    return obj.all()



@register.filter
def get_fields(obj):
    app_label = obj._meta.app_label
    field_names = [field.name for field in obj._meta.get_fields()]

    fields = []

    for field_name in field_names:
        print('[INFO] Resolving field: {}'.format(field_name))

        FIELDS_FAILING = []

        if field_name in FIELDS_FAILING:
            print('[WARN] Failed to resolve.')
            resp = {'value': 'FIELD LOOK-UP FAILED!!!'}

        # Check for reverse foreign-key properties first
        elif getattr(obj, '{}_set'.format(field_name), False):
            print('[INFO] Looking up RFK objects.')
            display_name, resp = _get_reverse_fk_set(obj, field_name)
        else:
            print('[INFO] Normal lookup.')
            display_name = field_name 
            value = getattr(obj, field_name, "-")

            if isinstance(value, models.Model):
                url = _get_obj_link(value, app_label=app_label)
                resp = {'value': value, 'url': url}
            elif isinstance(value, list):
                pk_url_list = _get_obj_links_list(field_name, value, app_label)
                resp = {'pk_url_list': pk_url_list}
            else:
                resp = {'value': value}

        fields.append((display_name, resp))

    return fields


@register.filter
def title_sentence_case(s):
    return stringcase.sentencecase(s).title() 


@register.filter
def to_class_name(obj):
    return obj.__class__.__name__
