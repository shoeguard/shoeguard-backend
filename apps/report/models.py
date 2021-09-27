from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.user.models import User


class Report(BaseModel):
    class ReportedDeviceType(models.TextChoices):
        IOT = 'IOT', _('IOT')
        PHONE = 'PHONE', _('PHONE')

    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True)
    reported_device = models.CharField(
        max_length=5,
        choices=ReportedDeviceType.choices,
    )
    is_done = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        reporter: User = self.reporter
        if reporter.parent is None:
            raise ValueError("Reporter must have a parent")
        super(Report, self).save(*args, **kwargs)
