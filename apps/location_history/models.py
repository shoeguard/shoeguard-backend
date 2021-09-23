from django.db import models

from apps.common.models import BaseModel
from apps.user.models import User


class LocationHistory(BaseModel):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
