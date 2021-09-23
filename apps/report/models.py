from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.user.models import ParentChildPair, User


class Report(BaseModel):
    class ReportedDeviceType(models.TextChoices):
        IOT = 'IOT', _('IOT')
        PHONE = 'PHONE', _('PHONE')

    parent_child_pair = models.ForeignKey(
        ParentChildPair,
        on_delete=models.CASCADE,
        null=True,
    )
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    audio_url = models.URLField(null=True)
    reported_device = models.CharField(
        max_length=5,
        choices=ReportedDeviceType.choices,
    )
