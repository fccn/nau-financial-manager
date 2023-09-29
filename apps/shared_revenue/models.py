from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.utils.translation import gettext_lazy as _

from apps.billing.models import Receipt
from apps.organization.models import Organization
from apps.util.models import BaseModel


class PartnershipLevel(BaseModel):
    """
    A model representing a partnership level.
    """

    name = models.CharField(_("Name"), max_length=50, unique=True)
    description = models.CharField(_("Description"), max_length=255, null=True, blank=True)
    
    # percentage that the organization will receive by the product/course sold on the receipt item.
    # Example by default will be read from a setting an the default setting value will be 70%.
    percentage = models.DecimalField(
        _("Value"),
        max_digits=3,
        validators=[MaxValueValidator(1), MinValueValidator(0)],
        decimal_places=2,
        unique=True,
    )
    # add new field
    # default boolean
    # only 1 PartnershipLevel can be default at the same time

    class Meta:
        verbose_name = _("Partnership level")
        verbose_name_plural = _("Partnership levels")

    def __str__(self) -> str:
        return f"{self.name} - {self.percentage}"

# Examples PartnershipLevel:
# id | description  | percentage | default
# 1  | default 2023 | 0.70       | true
# 2  | 30%          | 0.30       | false
# 3  | 40%          | 0.40       | false



# Organization
# Receipt --> Transaction  |-> rename
#   type of transaction |-> add this to the specification
# Receipt item --> line item  |-> rename

# Renames:
# course_id ==> product_id
#

class RevenueCourseConfiguration(BaseModel): ## RevenueProductConfiguration
    """
    A model representing a revenue configuration for an organization and partnership level.

    Example, 1 course with only 1 organization (its primary),
    The INA organization will receive the 70% from all transactions:
    | organization | course                          | partnership_level
    | INA          | course-v1:INA+XPTO+2021_T3      | 70%
    
    Example, 1 course with 2 organizations,
    The UNorteX is a consortium of 2 organizations. 
    The UPorto will receive 40% and its partner UMinho will receive 30%:
    | organization | course                          | partnership_level
    | UPorto       | course-v1:UNorteX+ABCD+2023_T3  | 40%
    | UMinho       | course-v1:UNorteX+ABCD+2023_T3  | 30%

    Example, 1 course with 2 organizations,
    INA has a course shared with USalamanca.
    The INA will receive 50% and its partner USalamanca will receive 20%:
    | organization | course                          | partnership_level
    | INA          | course-v1:INA+ASDF+2020_T3      | 50%
    | USalamanca   | course-v1:INA+ASDF+2020_T3      | 20%
    """

    # create a static method to verify if there isn't a date with the sum of all percentages > 100%
    # to be called on RevenueProductConfiguration.save() via admin

    # getActiveRevenueProductConfiguration(transaction datetime)

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="revenue_organizations", null=True, blank=True
    )

    product_id # string

    partnership_level = models.ForeignKey(
        PartnershipLevel, on_delete=models.CASCADE, related_name="revenue_partnership_levels"
    )
    start_date = models.DateTimeField(_("Start date"), auto_now_add=True)
    end_date = models.DateTimeField(_("End date"), null=True, blank=True)

    class Meta:
        verbose_name = _("Revenue configuration")
        verbose_name_plural = _("Revenue configurations")
        constraints = [
            # Please comment what this constraint is
            CheckConstraint(
                check=(
                    ~(Q(course_code__isnull=True) & Q(organization__isnull=True))
                    & ~(Q(course_code__exact="") & Q(organization__isnull=True))
                    & (
                        (Q(course_code__isnull=True) & Q(organization__isnull=False))
                        | (Q(course_code__isnull=False) & Q(organization__isnull=True))
                    )
                ),
                name="organization_and_course_code_not_null",
            )
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


#
