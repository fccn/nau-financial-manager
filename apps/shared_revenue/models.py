from datetime import datetime, timezone

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

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
        _("Partner percentage"),
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
        if self.start_date is None or self.end_date is None:
            return True

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

    def check_each_configuration(
        self,
        configuration,
    ) -> bool:
        if configuration.id == self.id:
            return True

        now = datetime.now(timezone.utc)
        saved_start_date = configuration.start_date
        saved_end_date = configuration.end_date
        start_date_to_save = self.start_date
        end_date_to_save = self.end_date

        if saved_start_date is None:
            if start_date_to_save is None or start_date_to_save > now:
                return False

            if end_date_to_save is None or end_date_to_save > now:
                return False

        if start_date_to_save is None:
            invalid_saved_end_date = saved_end_date is None or saved_end_date > now
            if saved_start_date < now and invalid_saved_end_date:
                return False

        if saved_end_date is None:
            return False

        if saved_end_date > start_date_to_save and saved_start_date < end_date_to_save:
            return False

        return True

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

        try:
            same_configurations: list[RevenueConfiguration] = RevenueConfiguration.objects.filter(
                **{
                    "organization": self.organization,
                    "product_id": self.product_id,
                }
            )
            for configuration in same_configurations:
                assert self.check_each_configuration(configuration=configuration)

            return False
        except Exception:
            raise ValidationError("There is a concurrent revenue configuration in this moment")

    def _check_partner_percentage(self) -> None:
        try:
            same_configurations: list[RevenueConfiguration] = RevenueConfiguration.objects.filter(
                product_id=self.product_id
            )

            percentages = self.partner_percentage
            for configuration in same_configurations:
                if configuration.id == self.id:
                    continue

                percentages = percentages + configuration.partner_percentage

            assert percentages <= 1
        except Exception:
            raise ValidationError("The partner percentage exceeds 100%")

    def validate_instance(self) -> None:
        try:
            validations = [
                self.has_concurrent_revenue_configuration,
                self._check_partner_percentage,
            ]

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
