from datetime import datetime, time

from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.organization.models import Organization


class SplitRevenueExportForm(forms.Form):
    """
    The parameters used to export the split revenue report.
    """

    start_date = forms.DateField(
        label=_("Start date"),
        widget=forms.DateInput(attrs={"type": "date"}),
        help_text=_("First day of the period, included."),
    )
    end_date = forms.DateField(
        label=_("End date"),
        widget=forms.DateInput(attrs={"type": "date"}),
        help_text=_("Last day of the period, included."),
    )
    organization = forms.ModelChoiceField(
        label=_("Organization"),
        queryset=Organization.objects.order_by("short_name"),
        required=False,
        empty_label=_("All organizations"),
    )
    product_id = forms.CharField(
        label=_("Product Id"),
        max_length=50,
        required=False,
        help_text=_("Optional, export only this product. Example: course-v1:ORG+COURSE+2024_T1"),
    )

    def clean(self) -> dict:
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date and end_date and end_date < start_date:
            self.add_error("end_date", _("The end date can not be before the start date."))

        return cleaned_data

    @property
    def period(self) -> tuple[datetime, datetime]:
        """
        The period to export, from the first moment of the start date to the last moment of the end date.
        """
        return (
            timezone.make_aware(datetime.combine(self.cleaned_data["start_date"], time.min)),
            timezone.make_aware(datetime.combine(self.cleaned_data["end_date"], time.max)),
        )

    @property
    def filters(self) -> dict:
        """
        The optional filters, in the format expected by the split services.
        """
        filters = {}
        if self.cleaned_data.get("organization"):
            filters["organization_code"] = self.cleaned_data["organization"].short_name
        if self.cleaned_data.get("product_id"):
            filters["product_id"] = self.cleaned_data["product_id"]

        return filters
