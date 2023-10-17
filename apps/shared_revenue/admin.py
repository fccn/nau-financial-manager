from django.contrib import admin

from apps.shared_revenue.models import RevenueConfiguration


class RevenueConfigurationAdmin(admin.ModelAdmin):
    list_display = ("organization", "course_code", "partner_percentage", "start_date", "end_date")
    search_fields = ("organization", "course_code", "partner_percentage", "start_date", "end_date")
    list_filter = ("created_at", "updated_at")


admin.site.register(RevenueConfiguration)
