from django.contrib import admin
from .models import PartyRecord,MillsRecord,InterestEntry,AllRecords,LedgerEntry
from import_export.admin import ImportExportModelAdmin

admin.site.register(LedgerEntry,ImportExportModelAdmin)
admin.site.register(PartyRecord,ImportExportModelAdmin)
admin.site.register(MillsRecord,ImportExportModelAdmin)


class InterestEntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'transaction_type', 'interest_rate', 'date', 'is_paid')
admin.site.register(InterestEntry, ImportExportModelAdmin)

class AllRecordsAdmin(admin.ModelAdmin):
    list_display = ['kl_no', 'party_name', 'mill_name', 'date']
    search_fields = ['kl_no', 'party_name', 'mill_name']
admin.site.register(AllRecords, ImportExportModelAdmin)

class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ('transaction_date', 'name', 'amount', 'party_or_mill', 'ac_name', 'created_at', 'payment_status')
    list_filter = ('transaction_date', 'party_or_mill', 'payment_status')
    search_fields = ('name', 'ac_name')

