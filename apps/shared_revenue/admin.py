from django.contrib import admin

from apps.shared_revenue.models import PartnershipLevel, RevenueConfiguration, ShareExecution


class PartnershipLevelAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "percentage", "created_at", "updated_at")
    search_fields = ("name", "description", "percentage")
    list_filter = ("created_at", "updated_at")


class RevenueConfigurationAdmin(admin.ModelAdmin):
    list_display = ("organization", "course_code", "partnership_level", "start_date", "end_date")
    search_fields = ("organization", "course_code", "partnership_level", "start_date", "end_date")
    list_filter = ("created_at", "updated_at")


class ShareExecutionAdmin(admin.ModelAdmin):
    list_display = ("organization", "course_code", "partnership_level", "start_date", "end_date")
    search_fields = ("organization", "course_code", "partnership_level", "start_date", "end_date")
    list_filter = ("created_at", "updated_at")


admin.site.register(PartnershipLevel)
admin.site.register(RevenueConfiguration)
admin.site.register(ShareExecution)
