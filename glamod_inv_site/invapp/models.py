# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Contact(models.Model):
 
    name = models.CharField(max_length=256, verbose_name='Contact Name')
    organisation = models.CharField(max_length=256, blank=True, null=True, verbose_name='Contact Organisation')

    class Meta:
        verbose_name = 'Contact'
        app_label = 'invapp'

    def __str__(self):
        return '{} ({})'.format(self.name, self.organisation)

class Inventory(models.Model):

    product_name = models.CharField(max_length=256, blank=True, null=True, verbose_name='Name')
    source_id = models.CharField(primary_key=True, max_length=256, verbose_name='Short name of source')
    product_id = models.CharField(max_length=256, blank=True, null=True, verbose_name='Id for source')

#    contact = models.TextField(blank=True, null=True, verbose_name='Contact details')  # This field type is a guess.
    contact = models.ForeignKey('Contact', blank=True, null=True, verbose_name='Contact')
    contact_role = models.TextField(blank=True, null=True)  # This field type is a guess.
    organisation = models.TextField(blank=True, null=True) 

    product_code = models.CharField(max_length=256, blank=True, null=True)
    product_version = models.CharField(max_length=256, blank=True, null=True)
    product_uri = models.CharField(max_length=256, blank=True, null=True)

    description = models.CharField(max_length=256, blank=True, null=True)
    product_references = models.TextField(blank=True, null=True, verbose_name='Paper citation')
    product_citation = models.TextField(blank=True, null=True, verbose_name='Product citation')

    start_date = models.DateTimeField(verbose_name='Start date')
    end_date = models.DateTimeField(verbose_name='End date')

    bbox_max_latitude = models.FloatField(verbose_name='Northern-most latitude')
    bbox_min_latitude = models.FloatField(verbose_name='Southern-most latitude')
    bbox_max_longitude = models.FloatField(verbose_name='Eastern-most longitude')
    bbox_min_longitude = models.FloatField(verbose_name='Western-most longitude')

    source_format_version = models.CharField(max_length=256, blank=True, null=True)
    source_file = models.CharField(max_length=256, blank=True, null=True)
    source_file_checksum = models.CharField(max_length=256, blank=True, null=True)

    data_policy_document = models.URLField(max_length=256, blank=True, null=True, verbose_name='URL to Data Policy document')

    total_station_count = models.IntegerField(verbose_name='Estimated station count')
    data_centre_url = models.URLField(max_length=256, blank=True, null=True)
    history = models.CharField(max_length=256, blank=True, null=True)

    comments = models.CharField(max_length=256, blank=True, null=True, verbose_name='Extra notes')
    timestamp = models.DateTimeField(blank=True, null=True)


    class Meta:
        verbose_name = 'Inventory'
        app_label = 'invapp'

    def __str__(self):
        return '{} ({})'.format(self.product_name, self.source_id)

