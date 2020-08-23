from django.dispatch import receiver
from openwisp_notifications.signals import notify
from swapper import load_model

from .signals import config_status_changed, device_registered

Config = load_model('config', 'Config')
Device = load_model('config', 'Device')


@receiver(
    config_status_changed,
    sender=Config,
    dispatch_uid='config_status_error_notification',
)
def config_status_error_notification(sender, instance, **kwargs):
    """
    Creates notification when status of a configuration changes to "error".
    """
    if instance.status == 'error':
        notify.send(sender=instance, type='config_error', target=instance.device)


@receiver(
    device_registered, sender=Config, dispatch_uid='device_registered_notification'
)
def device_registered_notification(sender, instance, **kwargs):
    """
    Creates notification when a new device is registered automatically
    through controller.
    """
    notify.send(sender=instance, type='device_registered', target=instance)
