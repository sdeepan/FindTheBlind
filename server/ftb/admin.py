from ftb.models import Patient, Address, PatientDetails, FamilyHistory
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User as AuthUser
from django.contrib.sites.models import Site
from ftb.adminsite.adminforms import FamilyHistoryForm
from locking.admin import LockableAdmin
from ftb.adminsite.modeladmin import TabbedModelAdmin
from settings import ADMIN_MEDIA_PREFIX

admin.site.unregister(AuthUser)
admin.site.unregister(Group)
admin.site.unregister(Site)

class PatientDetailsInline(admin.StackedInline):
    model = PatientDetails
    exclude = ('version',)
    verbose_name = 'Patient Details'
    verbose_name_plural = 'Patient Details'
    template = 'admin/edit_inline/stacked_one2one.html'
 
class AddressInline(admin.StackedInline):
    model = Address
    exclude = ('version',)    
    verbose_name = 'Address'
    verbose_name_plural = 'Address'
    template = 'admin/edit_inline/stacked_one2one.html'

class FamilyHistoryInline(admin.StackedInline):
    model = FamilyHistory
    exclude = ('version',)    
    verbose_name = 'Family history'
    verbose_name_plural = 'Family history'
    template = 'admin/edit_inline/stacked_one2one.html'
    form = FamilyHistoryForm
    
class PatientAdmin(TabbedModelAdmin, LockableAdmin):

    list_display = ('name', 'home_town', 'lock')
    search_fields = ('name', 'address__town')
    list_filter = ('address__town', 'patientdetails__gender')
    
    fieldsets = [
        (None, {'fields': ['name']}),
    ]

    tabs = {'Patient Details' : {'fieldsets': fieldsets, 'inlines' : (AddressInline, PatientDetailsInline)}, 'Family History' : {'fieldsets' : [], 'inlines' : (FamilyHistoryInline,)}}
    tabs_order = ('Patient Details', 'Family History')
    
    def home_town(self, obj):
        return obj.address.town
    home_town.short_description = 'Town/Village'

    class Media:
        js = (ADMIN_MEDIA_PREFIX + 'js/jquery.min.js',
              ADMIN_MEDIA_PREFIX + 'js/jquery.init.js',
              ADMIN_MEDIA_PREFIX + 'js/inlines.min.js',
              'ftb/js/jquery-ui-min.js',
              'ftb/js/admin.js',
              'ftb/js/fielddeps.js',)
        
        css = {'all': ('ftb/css/jquery-ui.css',)}
admin.site.register(Patient, PatientAdmin)


