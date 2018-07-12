from django.contrib import admin
from .models import Inventory, Contact


class InventoryAdmin(admin.ModelAdmin):
    model = Inventory

    extra_list_display = []
    extra_list_filter = []
    extra_search_fields = []
    list_editable = []
    raw_id_fields = []
    inlines = []
    filter_vertical = []
    filter_horizontal = []
    radio_fields = {}
    prepopulated_fields = {}
    formfield_overrides = {}
    readonly_fields = []

class ContactAdmin(admin.ModelAdmin):
    model = Contact



admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Contact, ContactAdmin)
