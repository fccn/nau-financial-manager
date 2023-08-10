from django.db import models

from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE


class StandardDefaults(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True