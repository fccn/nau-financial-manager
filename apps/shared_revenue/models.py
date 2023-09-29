from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.billing.models import Product, Receipt
from apps.organization.models import Organization
from apps.util.models import BaseModel


class PartnershipLevel(BaseModel):
    """
    A model representing a partnership level.

    The field percentage is the product price amount divided for each organization, the default percentage
    is 70% and if there are more than one organzation for this product, the value of 70% will be divided
    as the business partnership contract works

    """

    name = models.CharField(_("Name"), max_length=50, unique=True)
    description = models.CharField(_("Description"), max_length=255, null=True, blank=True)
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

    start_date = models.DateTimeField(_("Start date"), auto_now_add=True)
    end_date = models.DateTimeField(_("End date"), null=True, blank=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="revenue_organizations", null=True, blank=True
    )
    partnership_level = models.ForeignKey(
        PartnershipLevel, on_delete=models.CASCADE, related_name="revenue_partnership_levels"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="revenue_product", null=True, blank=True
    )

    class Meta:
        verbose_name = _("Revenue configuration")
        verbose_name_plural = _("Revenue configurations")
        constraints = [
            # CheckConstraint(
            #     check=(
            #         ~(Q(course_code__isnull=True) & Q(organization__isnull=True))
            #         & ~(Q(course_code__exact="") & Q(organization__isnull=True))
            #         & (
            #             (Q(course_code__isnull=True) & Q(organization__isnull=False))
            #             | (Q(course_code__isnull=False) & Q(organization__isnull=True))
            #         )
            #     ),
            #     name="organization_and_course_code_not_null",
            # )
        ]

    def __str__(self) -> str:
        return f"{self.organization} - {self.course_code} - {self.partnership_level}"


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
