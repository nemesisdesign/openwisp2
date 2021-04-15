from django.urls import path

from . import consumers as ow_consumer


def get_routes(consumer=ow_consumer):
    return [path('ws/device/<uuid:pk>/command', consumer.CommandConsumer)]
