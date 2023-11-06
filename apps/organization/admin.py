from django.contrib import admin

from apps.organization.models import Organization


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "email", "created_at", "updated_at", "is_active")
    search_fields = ("name", "email", "short_name")


admin.site.register(Organization, OrganizationAdmin)
