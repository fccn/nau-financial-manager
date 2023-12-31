from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel


class BaseModel(SafeDeleteModel):
    """
    Abstract base model that provides common fields for all models in the project.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class CustomUser(AbstractUser):
    """
    Custom user model that extends the built-in Django user model.
    """

    uuid = models.UUIDField("uuid", default=uuid4, editable=False)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.email
