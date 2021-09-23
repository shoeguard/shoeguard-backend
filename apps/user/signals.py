from os import environ

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from twilio.rest import Client

from apps.user.models import Auth


@receiver(post_save, sender=Auth)
def send_sms_post_save_handler(
    sender,
    instance: Auth,
    created: bool,
    **kwargs,
):
    if 'test' in environ['DJANGO_SETTINGS_MODULE']:
        return
    if created and not instance.is_verified:
        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN,
        )

        client.messages.create(
            body=f'[슈가드] 인증번호: {instance.code}',
            from_='+19168238724',
            to=f'+82{instance.phone_number[1:]}',
        )
