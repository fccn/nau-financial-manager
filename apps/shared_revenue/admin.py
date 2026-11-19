import logging
from io import BytesIO

from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.http import FileResponse
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.translation import gettext_lazy as _

from apps.shared_revenue.forms import SplitRevenueExportForm
from apps.shared_revenue.models import RevenueConfiguration
from apps.shared_revenue.services.split_export import SplitExportService

logger = logging.getLogger("nau_financial_manager")


class RevenueConfigurationAdmin(admin.ModelAdmin):
    list_display = ("organization", "product_id", "partner_percentage", "start_date", "end_date")
    search_fields = ("organization__short_name", "organization__name", "product_id")
    list_filter = ("created_at", "updated_at")
    change_list_template = "admin/shared_revenue/revenueconfiguration/change_list.html"

    def get_urls(self):
        urls = [
            path(
                "export-split-revenue/",
                self.admin_site.admin_view(self.export_split_revenue_view),
                name="shared_revenue_revenueconfiguration_export_split_revenue",
            ),
        ]

        return urls + super().get_urls()

    def has_export_permission(self, request) -> bool:
        return request.user.has_perm("shared_revenue.export_split_revenue")

    def changelist_view(self, request, extra_context=None):
        extra_context = {**(extra_context or {}), "has_export_permission": self.has_export_permission(request)}

        return super().changelist_view(request, extra_context=extra_context)

    def export_split_revenue_view(self, request):
        """
        Displays the form to choose the parameters of the split revenue report and,
        when it is submitted, delivers the report as a xlsx file to be downloaded.
        """
        if not self.has_export_permission(request):
            raise PermissionDenied

        form = SplitRevenueExportForm(request.POST if request.method == "POST" else None)
        if form.is_valid():
            start_date, end_date = form.period
            report = SplitExportService().export_split_to_xlsx_content(
                start_date=start_date,
                end_date=end_date,
                **form.filters,
            )
            if report:
                file_name, content = report
                logger.info(
                    f"Split revenue report exported by {request.user.get_username()} using the parameters: "
                    f"start_date: {start_date}, end_date: {end_date}, options: {form.filters}"
                )

                return FileResponse(BytesIO(content), as_attachment=True, filename=file_name)

            self.message_user(
                request,
                _("There is no data to export using these parameters."),
                messages.WARNING,
            )

        context = {
            **self.admin_site.each_context(request),
            "opts": self.model._meta,
            "title": _("Export split revenue report"),
            "form": form,
        }

        return TemplateResponse(
            request,
            "admin/shared_revenue/revenueconfiguration/export_split_revenue.html",
            context,
        )


admin.site.register(RevenueConfiguration, RevenueConfigurationAdmin)
