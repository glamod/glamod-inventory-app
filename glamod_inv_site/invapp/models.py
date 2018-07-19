# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django import forms
from datetime import datetime
from django.utils import timezone
from uuid import uuid4




# ==========================================================
# Class / model to store documents
# ==========================================================
#class DocStore( models.Model ):
#    name        = models.CharField(max_length=256, null=False)
#    description = models.TextField()
#    sourceURL   = models.URLField()
#    cache       = models.BinaryField()
#    class Meta:
#        verbose_name = "document"
#        app_label    = "invapp"


# ==========================================================
# Model to represent CI_ResponsibleParty
# ==========================================================
class Contact(models.Model):
    name          = models.CharField(max_length=256, null=True, verbose_name='Contact Name')
    organisation  = models.CharField(max_length=256, null=True, verbose_name='Contact Organisation')
    emailAddress  = models.EmailField(null=True, verbose_name="Email address")
    telephone     = models.CharField(max_length=20, null=True, verbose_name="Telephone (incl. country and area code)")
    address       = models.CharField(max_length=256, blank=True, null=True)
    city          = models.CharField(max_length=256, blank=True, null=True)
    adminArea     = models.CharField(max_length=256, blank=True, null=True)
    postalCode    = models.CharField(max_length=256, blank=True, null=True)
    country       = models.CharField(max_length=256, blank=True, null=True)
    privacy       = models.BooleanField( null = False, default = True) # Place holder field - GDPR !!!!!! Need to decide what to do.

    class Meta:
        verbose_name = 'Contact'
        app_label = 'invapp'
    def __str__(self):
        return '{} ({})'.format(self.name, self.organisation)
    def all(self):
        return Contact.objects.all()

# ==========================================================
# Model to store role codes
# ==========================================================
class CI_RoleCode(models.Model):
    entry          = models.CharField( max_length=32, verbose_name = 'Entry')
    description    = models.TextField( blank = True, null = True, verbose_name = 'Description')
    source         = models.CharField( max_length=8, null = False, verbose_name = 'Source of entry')
    applicable_for = models.TextField( null = True, blank=True) 


# ==========================================================
# Model to store inventory record (station level)
# ==========================================================
#class InventoryStation( models.Model ):
#    station_id            = models.CharField( max_length = 256 )
#    source_uid            = models.CharField( max_length = 256 ) # can a station come from more than one source?
#    source_name           = models.CharField( max_length = 256 )
#    data_repository_ftp   = models.CharField( max_length = 256 )
#    wmo_id                = models.CharField( max_length = 256 )
#    station_name          = models.CharField( max_length = 256 )
#    lat                   = models.CharField( max_length = 256 ) # what about mobile stations or station moves?
#    lon                   = models.CharField( max_length = 256 )
#    elev                  = models.CharField( max_length = 256 )
#    fips_code             = models.CharField( max_length = 256 )
#    country               = models.CharField( max_length = 256 )
#    continent             = models.CharField( max_length = 256 )
#    station_data_policy   = models.CharField( max_length = 256 )
#    station_data_type     = models.CharField( max_length = 256 )
#    data_update_status    = models.CharField( max_length = 256 )
#    station_metadata_link = models.CharField( max_length = 256 )
#    timestep              = models.CharField( max_length = 256 )
#    ver                   = models.CharField( max_length = 256 )
#    obs_freq              = models.CharField( max_length = 256 )
#    obs_time_GMT          = models.CharField( max_length = 256 )
#    start_year            = models.CharField( max_length = 256 )# per variable
#    end_year              = models.CharField( max_length = 256 )# per variable




# ==========================================================
# Model to store list of variables in source (better name needed for class)
# ==========================================================
#class variables_present( models.Model ):
#    source     = models.ForeignKey( 'Inventory', null = False )
#    var        = models.ForeignKey( 'variable', null = False ) # variable number from CDM?
#    status     = models.CharField( max_length = 256, null = False) # available, not available
#    date_start = models.DateTimeField()
#    date_end   = models.DateTimeField()

# ==========================================================
# Model to store inventory record (source level)
# ==========================================================
class Inventory(models.Model):
    source_id       = models.CharField(default = uuid4, primary_key=True, max_length=256, verbose_name='Unique ID for source') # source_uid | source_id
    product_name    = models.CharField(max_length=256, blank=True, null=True, verbose_name='Dataset name') # data_name | product_name
    product_id      = models.CharField(max_length=256, blank=True, null=True, verbose_name='Product ID (set by provider)') # | product_id
    record_status   = models.CharField(max_length=256, blank=True, null=True, verbose_name = 'Status of metadata record') # inventory version?
    product_code    = models.CharField(max_length=256, blank=True, null=True) # | product_code
    product_version = models.CharField(max_length=256, blank=True, null=True) # | product_version
    product_level   = models.CharField(max_length=256, blank=True, null=True) # | product_level
    product_status  = models.CharField(max_length=256, blank=True, null=True, verbose_name = 'Status of product') # | product_status

    
    contact_metadata      = models.ForeignKey('Contact', blank=True, null=True, verbose_name='Contact (for metadata)', related_name = 'contact_data')  # | contact
    contact_role_metadata = models.ForeignKey('CI_RoleCode', blank=True, null=True, verbose_name='Role (for metadata contact)', related_name = 'contact_role_data') # | contact_role
    #organisation_metadata = models.TextField(blank=True, null=True) # remove, part of contact?



    # description = HTMLField()
    description        = models.TextField(blank=True, null=True, verbose_name = 'Descripton / abstract') #  | description # change to tinyMCE editor?
    product_references = models.TextField(blank=True, null=True, verbose_name='Papers / references describing the data') # | product_references # link table?
    product_citation   = models.TextField(blank=True, null=True, verbose_name='Product citation (how to cite this data)') # | product_citation # text to be used for citing this source

    data_policy          = models.CharField(max_length=256, blank=True, null = True) # source_data_policy | data_policy_licence
    data_policy_document = models.URLField(max_length=256, blank=True, null=True, verbose_name='URL to Data Policy document') # do we want to cache the data policy document?
    # keywords (to be added)
    variables_attained     = models.CharField(max_length=256, null=True, blank=True)
    variables_not_attained = models.CharField(max_length=256, null=True, blank=True)
    
    # domain, reporting frequency etc
    spatial_domain      = models.CharField(max_length=256, null=True) # domain | # domain - data coverage (global, European, Asia etc)
    geometry_type       = models.CharField(max_length=256, null=True)
    crs                 = models.CharField(max_length=256, null=True)
    bbox_min_latitude   = models.FloatField(verbose_name='Southern-most latitude') # lat_min | bbox_lat_min
    bbox_max_latitude   = models.FloatField(verbose_name='Northern-most latitude') # lat_max | bbox_lat_max
    bbox_min_longitude  = models.FloatField(verbose_name='Western-most longitude') # lon_min | bbox_lon_min
    bbox_max_longitude  = models.FloatField(verbose_name='Eastern-most longitude') # lon_max | bbox_lon_max
    start_date          = models.DateTimeField(verbose_name='Start date')
    end_date            = models.DateTimeField(verbose_name='End date')
    station_count       = models.IntegerField(verbose_name='Estimated number of stations in dataset', blank=True, null=True)
    mean_years_present  = models.IntegerField(verbose_name='Mean number of years available (per station)', null=True)
    reporting_frequency = models.CharField(max_length=10, null=True, blank=True)


    data_centre           = models.CharField(max_length=256, blank=True, null=True) # | data_centre
    data_centre_url       = models.URLField(max_length=256, blank=True, null=True) # | data_centre_url
    source_format         = models.CharField(max_length=256, null=True) # | source_format
    source_format_version = models.CharField(max_length=256, blank=True, null=True) # | source_format_version
    source_file           = models.CharField(max_length=256, blank=True, null=True) # | source_file
    source_file_checksum  = models.CharField(max_length=256, blank=True, null=True) # | source_file_checksum
    contact_data          = models.ForeignKey('Contact', blank=True, null=True, verbose_name='Contact (for data)') # | contact
    contact_role_data     = models.ForeignKey('CI_RoleCode', blank=True, null=True, verbose_name='Role (for data)') # | contact_role
    product_uri           = models.CharField(max_length=256, blank=True, null=True) # | product_uri

    comments         = models.TextField(blank=True, null=True, verbose_name='Extra notes') # | comments
    timestamp        = models.DateTimeField(default = timezone.now, null=False, verbose_name = 'Time / date this metadata entry was last edited') # | timestamp
    history          = models.TextField(blank=True, null=True) # | history
    update_frequency = models.CharField( max_length = 256, null=True ) # data update status | maintenance_and_update_frequency
    optional_data    = models.BooleanField( default=False ) # | optional_data


    
    class Meta:
        verbose_name = 'Inventory'
        app_label = 'invapp'
        #model = FlatPage

    def __str__(self):
        return '{} ({})'.format(self.product_code, self.product_id, self.source_id)

    def all(self):
        return Inventory.objects.all()


    # dict to map fields in xls sheets
    def getDict(self):
        mydict =  {
            'source_id'              : 'SOURCE_UID',                    # example: 1000001
            'product_code'           : 'DATA_REPOSITORY',               # example: ghcnd
            'product_id'             : 'DATA_NAME',                     # example: ghcnd_australia
            'product_uri'            : 'Method of data transfer',       # example: ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/stage1/
            'data_centre'            : 'SOURCE_NAME',                   # example: national climate centre bureau of meteorology po box 1289k melbourne 3001
            'spatial_domain'         : 'DOMAIN',                        # example: australia
            'bbox_max_latitude'      : 'NORTH_BOUND',                   # example: -9.2
            'bbox_min_latitude'      : 'SOUTH_BOUND',                   # example: -43.7
            'bbox_min_longitude'     : 'WEST_BOUND',                    # example: 153.6
            'bbox_max_longitude'     : 'EAST_BOUND',                    # example: -34.8
            'data_policy_licence'    : 'SOURCE_DATA_POLICY',            # example: 103
            'variables_attained'     : 'ECVs_ATTAINED',                 # example: temp rain
            'variables_not_attained' : 'OTHER_VARIABLES_NOT ATTAINED',  # example: evap rain wbrh t_sun
            'reporting_frequency'    : 'TIMESTEP',                      # example: DY
            'start_date'             : 'DATA_FIRST_YEAR',               # example: 1882
            'end_date'               : 'DATA_LAST_YEAR',                # example: 2007
            'mean_years_present'     : 'DATA_MEAN_YEARS',               # example: 43
            'update_frequency'       : 'DATA_UPDATE_STATUS',            # example: daily updates
        }
        return mydict

    #'product_name'           : ''                              # example: Global Historical Climatology Network Daily
    #'': 'STATION_DECK_LINK'  # example: Daily_station_deck_inventory.xlsx