import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'glamod_inv_site.settings'
import random
import datetime

import django
django.setup()

print("Importing models...")
from invapp.models import *


def add_record(**kwargs):
    keys = 'source_id product_id product_name product_code product_version product_uri ' \
           'description product_references product_citation source_format_version ' \
           'source_file source_file_checksum data_centre_url contact contact_role ' \
           'history comments timestamp bbox_min_latitude bbox_min_longitude ' \
           'bbox_max_latitude bbox_max_longitude start_date end_date total_station_count'.split()

    special_fields = {'timestamp': datetime.datetime.now(),
                      'data_centre_url': 'http://www.ceda.ac.uk',
                      'bbox_min_latitude': -20, 
                      'bbox_max_latitude': 20,
                      'bbox_min_longitude': -20,
                      'bbox_max_longitude': 20,
                      'start_date': datetime.datetime(1900, 1, 1),
                      'end_date': datetime.datetime(2018, 1, 1),
                      'total_station_count': 1234}
    values = []

    for key in keys:
        if key in kwargs:
            value = kwargs[key]
        elif key in special_fields:
            value = special_fields[key]
        else:
            shuffled = [i for i in key]
            random.shuffle(shuffled)
            value = ''.join(shuffled) 

        values.append(value)

    items = dict([(keys[i], values[i]) for i in range(len(keys))])
    inv = Inventory.objects.create(**items)
    print('Count: {}'.format(Inventory.objects.count()))
    return inv


for i in range(5): 
    inv = add_record()
    print('Added inv: {}'.format(inv.source_id))
