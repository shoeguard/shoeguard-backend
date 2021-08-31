from django.db import models

from apps.common.models import BaseModel
from apps.user.models import ParentChildPair


class LocationHistory(BaseModel):
    parent_child_pair = models.ForeignKey(
        ParentChildPair,
        on_delete=models.CASCADE,
    )
    address = models.CharField(max_length=255, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)