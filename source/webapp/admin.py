from django.contrib import admin

from webapp.models import Issue


class TypeAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['title']
    list_display_links = ["title"]
    search_fields = ['title']
    fields = ['title']
    readonly_fields = ['title']


class StatusAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['title']
    list_display_links = ["title"]
    search_fields = ['title']
    fields = ['title']
    readonly_fields = ['title']


class IssueAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'statuses', 'summary']
    list_filter = ['statuses', 'id', 'types']
    list_display_links = ["description"]
    search_fields = ['description', 'statuses']
    fields = ['description', 'statuses']
    readonly_fields = ['types']


admin.site.register(Issue, IssueAdmin, TypeAdmin, StatusAdmin)
