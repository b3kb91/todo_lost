from django.contrib import admin

from webapp.models import Issue, Status, Type


class IssueAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'statuses', 'summary', 'types', 'created_at', 'updated_at']
    list_filter = ['statuses', 'id', 'types', 'statuses']
    list_display_links = ["description", 'statuses', 'types']
    search_fields = ['description', 'statuses', 'types']
    fields = ['description', 'statuses', 'types']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Issue, IssueAdmin)
admin.site.register(Status)
admin.site.register(Type)
