from django.contrib import admin

from webapp.models import Issue, Status, Type


class TypeInline(admin.TabularInline):
    model = Issue.types.through


class IssueAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'statuses', 'summary', 'created_at', 'updated_at']
    list_filter = ['statuses', 'id', 'statuses']
    list_display_links = ["description", 'statuses']
    search_fields = ['description', 'statuses']
    fields = ['description', 'statuses']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [
        TypeInline,
    ]


admin.site.register(Issue, IssueAdmin)
admin.site.register(Status)
admin.site.register(Type)
