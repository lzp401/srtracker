from django.contrib import admin
from recordlist.models import Record
from django.utils.translation import ugettext_lazy

# Register your models here.
class RecordAdmin(admin.ModelAdmin):
    list_display = ('srNumber', 'customer', 'description', 'openDate', 'calPriority', 'reviewRequired')
    readonly_fields = (
        'srNumber', 'customer', 'description', 'openDate', 'modifiedDate',
        'touchDate', 'closeDate', 'escalationLevel'
    )

    fieldsets = (
        ('', {
            'fields': ('srNumber',)
        }), ('Original Data Source', {
            'fields': ('description', 'openDate', 'modifiedDate',
                       'touchDate', 'closeDate', 'escalationLevel')
        }), ('SR Tracker', {
            'fields': ('calReviewDate', 'calSummary', 'overallStatus',
                       'calPriority', 'faultCategory', 'reviewRequired')
        })
    )


admin.site.site_header = ugettext_lazy('SR Tracker Administration')
admin.site.register(Record, RecordAdmin)