import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'glamod_inv_site.settings'

import django
django.setup()

print("Importing models...")
from invapp.models import *
from django.contrib.postgres.search import SearchVector

fields = ['station_name', 'source_record_id', 'platform_type__description']
term = 'Svend'

res = Inventory.objects.annotate(search=SearchVector(*fields)).filter(search__icontains=term)

for r in res: print(r)

print('{} records found'.format(len(res)))

