import pytest
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.utils import timezone
from openwisp2.routing import application

from ...connection.tests.utils import CreateCommandMixin


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestNotificationSockets(CreateCommandMixin):
    async def _get_communicator(self, admin_client, device_id):
        session_id = admin_client.cookies['sessionid'].value
        communicator = WebsocketCommunicator(
            application,
            path=f'ws/device/{device_id}/command',
            headers=[(b'cookie', f'sessionid={session_id}'.encode('ascii'),)],
        )
        connected, subprotocol = await communicator.connect()
        assert connected is True
        return communicator

    async def test_new_notification_created(self, admin_user, admin_client):
        device_conn = await database_sync_to_async(self._create_device_connection)()
        communicator = await self._get_communicator(admin_client, device_conn.device_id)
        command = await database_sync_to_async(self._create_command)(
            device_conn=device_conn
        )

        # No message should be sent through websocket for newly created command.
        assert await communicator.receive_nothing() is True

        command.status = 'success'
        await database_sync_to_async(command.save)()
        response = await communicator.receive_json_from()
        expected_response = {
            'model': 'Command',
            'data': {
                'id': str(command.id),
                'created': timezone.localtime(command.created).isoformat(),
                'modified': timezone.localtime(command.modified).isoformat(),
                'status': command.status,
                'type': 'Custom commands',
                'input': command.input_data,
                'output': command.output,
                'device': str(command.device_id),
                'connection': str(command.connection_id),
            },
        }
        assert response == expected_response
        await communicator.disconnect()
