from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.util.models import BaseModel


class Organization(BaseModel):
    """
    A model representing an organization.
    """

    name = models.CharField(_("Name"), max_length=255, null=True)
    short_name = models.CharField(_("Short Name"), max_length=50, db_index=True, null=True, unique=True)
    email = models.CharField(_("Email"), max_length=255, null=True)

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    def __str__(self) -> str:
        return f"{self.short_name}"
