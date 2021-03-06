from django.db import models

from apps.common.models import BaseModel
from apps.user.models import User


class LocationHistory(BaseModel):
    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        reporter: User = self.reporter
        if reporter.parent is None:
            raise ValueError("Reporter must have a parent")
        super(LocationHistory, self).save(*args, **kwargs)
