import json

from swapper import load_model

from ...config.base.channels_consumer import BaseConsumer

Device = load_model('config', 'Device')


class CommandConsumer(BaseConsumer):
    model = Device
    channel_layer_group = 'config.device'

    def send_update(self, event):
        event.pop('type')
        self.send(json.dumps(event))
