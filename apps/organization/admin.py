from django.contrib import admin

from apps.organization.models import Organization, OrganizationAddress, OrganizationContact


class OrganizationAddressInline(admin.TabularInline):
    model = OrganizationAddress
    extra = 0


class OrganizationContactInline(admin.TabularInline):
    model = OrganizationContact
    extra = 0


class OrganizationAdmin(admin.ModelAdmin):
    inlines = [
        OrganizationAddressInline,
        OrganizationContactInline,
    ]
    list_display = ("name", "short_name", "created_at", "updated_at", "is_active")
    search_fields = ("name", "slug", "short_name")


admin.site.register(Organization, OrganizationAdmin)
