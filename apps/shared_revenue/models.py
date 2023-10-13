from datetime import datetime, timezone

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.billing.models import Receipt
from apps.organization.models import Organization
from apps.util.models import BaseModel


class RevenueConfiguration(BaseModel):
    """
    A model representing a revenue configuration for an organization.
    """

    start_date = models.DateTimeField(_("Start date"), null=True, blank=True)
    end_date = models.DateTimeField(_("End date"), null=True, blank=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="revenue_organizations", null=True, blank=True
    )
    partner_percentage = models.DecimalField(
        _("Value"),
        default=0.70,
        max_digits=3,
        validators=[MaxValueValidator(1), MinValueValidator(0)],
        decimal_places=2,
    )

    product_id = models.CharField(_("Product Id"), max_length=50, null=False)

    class Meta:
        verbose_name = _("Revenue configuration")
        verbose_name_plural = _("Revenue configurations")

    @property
    def status(self) -> bool:
        """
        Check if the revenue configuration is still in vigency.
        """
        today = datetime.now()
        if today <= self.end_date:
            try:
                self.objects.get(
                    organization=self.organization,
                    product_id=self.product_id,
                    start_date__lte=self.end_date,
                    end_date__gte=self.start_date,
                )

                return True
            except ObjectDoesNotExist:
                return False
        return False

    def has_concurrent_revenue_configuration(self) -> bool:
        """
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
        if self.start_date is None or self.end_date is None:
            return True

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

                    reference_date = self.start_date if not self_start_date_is_empty else datetime.now(timezone.utc)
                    current_start_date = revenue_configuration.start_date

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

                    current_end_date = revenue_configuration.end_date

                    # if finished_revenue_configuration, it means this RevenueConfiguration is old
                    finished_revenue_configuration: bool = current_end_date < reference_date

                    return finished_revenue_configuration

                assert check_each_configuration()

            return False
        except Exception as e:
            e
            raise ValidationError("There is a concurrent revenue configuration in this moment")

    def validate_instance(self) -> None:
        try:
            validations = [self.has_concurrent_revenue_configuration]
            for validation in validations:
                validation()
        except Exception as e:
            raise e

    def save(self, keep_deleted=False, **kwargs):
        try:
            self.validate_instance()
            return super().save(keep_deleted, **kwargs)
        except Exception as e:
            raise e

    def __str__(self) -> str:
        return f"{self.organization} - {self.product_id} - {self.partner_percentage}"


class ShareExecution(BaseModel):
    """
    A model representing a share execution for an organization.
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
