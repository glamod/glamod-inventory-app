import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'glamod_inv_site.settings'

import django
django.setup()

print("Importing models...")
from invapp.models import *

x = Inventory.objects.first()
print(x)
print(x._meta)


