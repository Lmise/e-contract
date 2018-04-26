from django.contrib import admin
from .models import Contract

class ContractAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'slug', 'project_publish_date', 'project_status')
    list_filter = ('project_status', 'project_publish_date','project_holder')
    search_fields = ('project_name', 'project_description')
    prepopulated_fields = {'slug' : ('project_name',)}
    raw_id_fields = ('project_holder',)
    date_hierarchy = 'project_publish_date'
    ordering = ['project_status', 'project_publish_date']


admin.site.register(Contract, ContractAdmin)


