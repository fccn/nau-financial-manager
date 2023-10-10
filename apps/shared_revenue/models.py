from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.billing.models import Receipt
from apps.organization.models import Organization
from apps.util.models import BaseModel


class PartnershipLevel(BaseModel):
    """
    A model representing a partnership level.

    The field percentage is the product price amount divided for each organization, the default percentage
    is 70% and if there are more than one organzation for this product, the value of 70% will be divided
    as the business partnership contract works

    """

    name = models.CharField(_("Name"), default="Silver", max_length=50, unique=True)
    description = models.CharField(
        _("Description"),
        default="Partnership level default of 70% percent of earning for the course",
        max_length=255,
        null=True,
        blank=True,
    )
    percentage = models.DecimalField(
        _("Value"),
        default=0.70,
        max_digits=3,
        validators=[MaxValueValidator(1), MinValueValidator(0)],
        decimal_places=2,
        unique=True,
    )

    class Meta:
        verbose_name = _("Partnership level")
        verbose_name_plural = _("Partnership levels")

    def __str__(self) -> str:
        return f"{self.name} - {self.percentage}"


class RevenueConfiguration(BaseModel):
    """
    A model representing a revenue configuration for an organization and partnership level.
    """

    start_date = models.DateTimeField(_("Start date"), null=True, blank=True)
    end_date = models.DateTimeField(_("End date"), null=True, blank=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="revenue_organizations", null=True, blank=True
    )
    partnership_level = models.ForeignKey(
        PartnershipLevel, on_delete=models.CASCADE, related_name="revenue_partnership_levels"
    )
    product_id = models.CharField(_("Product Id"), max_length=50, null=False)

    class Meta:
        verbose_name = _("Revenue configuration")
        verbose_name_plural = _("Revenue configurations")

    def make_date_as_comparable(self, date: datetime) -> int:
        return int(str(date.date()).replace("-", ""))

    def has_concurrent_revenue_configuration(self) -> bool:
        """
        Validates if exists a concurrent RevenueConfiguration with the same parameters

        A councurrent RevenueConfiguration is checked by the available period of running
        based on the product_id and organization parameters

        The concept of concurrent is available, it means if this method returns True,
        it's not possible to register a new RevenueConfiguration, because for this period
        there is an available RevenueConfiguration running

        Returns:
            bool: If a concurrent RevenueConfiguration exists it must return True, otherwise False

        Conditions:

            True:
                if start_date < self.start_date and end_date null or blank
                if start_date < self.start_date and end_date > self.end_date

            False:
                if start_date > self.start_date and end_date null or blank
                if start_date < self.start_date and end_date < self.end_date

        """

        try:
            same_configurations: list[RevenueConfiguration] = RevenueConfiguration.objects.filter(
                **{
                    "organization": self.organization,
                    "product_id": self.product_id,
                }
            )

            self_start_date_is_empty: bool = str(self.start_date).lstrip() in ["", "None"]
            for revenue_configuration in same_configurations:

                def check_each_configuration() -> bool:
                    start_date_is_empty: bool = str(revenue_configuration.start_date).lstrip() in ["", "None"]

                    # validade if the attempt is to insert more than one None or blank start_date
                    # if pass, it means the attempt is to edit the current register
                    if start_date_is_empty:
                        self_id: int = self.id if self.id is not None else -1
                        self_is_loop_current_instance: bool = revenue_configuration.id is self_id
                        if self_start_date_is_empty and not self_is_loop_current_instance:
                            return False

                        # if self.start_date is None or blank it can continue because it's saving in the same register
                        # it will save from None/blank to None/blank
                        return True

                    reference_date = self.start_date if not self_start_date_is_empty else datetime.now()
                    reference_date = self.make_date_as_comparable(date=reference_date)
                    current_start_date = self.make_date_as_comparable(date=revenue_configuration.start_date)

                    # if future_start_date, it means this RevenueConfiguration is not available to run yet
                    future_start_date: bool = current_start_date > reference_date
                    if future_start_date:
                        return True

                    # if revenue_configuration_end_date_is_empty, it means this RevenueConfiguration is concurrent
                    revenue_configuration_end_date_is_empty: bool = str(revenue_configuration.end_date).lstrip() in [
                        "",
                        "None",
                    ]
                    if revenue_configuration_end_date_is_empty:
                        return False

                    current_end_date = self.make_date_as_comparable(date=revenue_configuration.end_date)
                    # if finished_revenue_configuration, it means this RevenueConfiguration is old
                    finished_revenue_configuration: bool = future_start_date or current_end_date < reference_date

                    return finished_revenue_configuration

                assert check_each_configuration()

            return False
        except Exception as e:
            e
            raise ValidationError("There is a concurrent revenue configuration in this moment")

    validations = [has_concurrent_revenue_configuration]

    def __str__(self) -> str:
        return f"{self.organization} - {self.product_id} - {self.partnership_level}"


class ShareExecution(BaseModel):
    """
    A model representing a share execution for an organization and partnership level.
    """

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="share_organizations")
    revenue_configuration = models.JSONField(_("Revenue Configuration"))
    percentage = models.DecimalField(_("Percentage"), max_digits=5, decimal_places=2)
    value = models.DecimalField(_("Value"), max_digits=5, decimal_places=2)
    receipt = models.CharField(Receipt, max_length=50)
    executed = models.BooleanField(_("Executed"), default=False)
    response_payload = models.JSONField(_("Response Payload"))

    class Meta:
        verbose_name = _("Share exectution")
        verbose_name_plural = _("Share exectutions")

    def __str__(self) -> str:
        return f"{self.organization} - {self.revenue_configuration} - {self.percentage}"
