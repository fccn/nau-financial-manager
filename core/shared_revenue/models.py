from django.db import models

from core.util.models import BaseModel
from core.organization.models import Organization
from django.utils.translation import gettext_lazy as _


class PartnershipLevel(BaseModel):
    name = models.CharField(_('Name'), max_length=50)
    description = models.CharField(_('Description'), max_length=255, null=True, blank=True)
    value = models.DecimalField(_('Value'), max_digits=5, decimal_places=2)
    
    class Meta:
        verbose_name = _('Partnership level')
        verbose_name_plural = _('Partnership levels')


class RevenueConfiguration(BaseModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='revenue_organizations')
    partnership_level = models.ForeignKey(PartnershipLevel, on_delete=models.CASCADE, related_name='revenue_partnership_levels')
    start_date = models.DateField(_('Start date'), auto_now_add=True)
    end_date = models.DateField(_('End date'), null=True, blank=True)

    class Meta:
        verbose_name = _('Revenue configuration')
        verbose_name_plural = _('Revenue configurations')


class ShareExecution(BaseModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='share_organizations')
    partnership_level = models.CharField(_('Partnership level'), max_length=50)
    percentage = models.DecimalField(_('Percentage'), max_digits=5, decimal_places=2)
    value = models.DecimalField(_('Value'), max_digits=5, decimal_places=2)
    # receipts = models.ManyToManyField('Receipt', related_name='share_receipts')
    executed = models.BooleanField(_('Executed'), default=False)