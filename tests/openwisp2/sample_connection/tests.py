from openwisp_controller.connection.tests.test_admin import (
    TestCommandInlines as BaseTestCommandInlines,
)
from openwisp_controller.connection.tests.test_admin import (
    TestConnectionAdmin as BaseTestConnectionAdmin,
)
from openwisp_controller.connection.tests.test_models import (
    TestModels as BaseTestModels,
)
from openwisp_controller.connection.tests.test_models import (
    TestModelsTransaction as BaseTestModelsTransaction,
)
from openwisp_controller.connection.tests.test_notifications import (
    TestNotifications as BaseTestNotifications,
)
from openwisp_controller.connection.tests.test_ssh import TestSsh as BaseTestSsh
from openwisp_controller.connection.tests.test_tasks import TestTasks as BaseTestTasks


class TestConnectionAdmin(BaseTestConnectionAdmin):
    config_app_label = 'sample_config'
    app_label = 'sample_connection'


class TestCommandInlines(BaseTestCommandInlines):
    config_app_label = 'sample_config'

    def test_notification_host_setting(self):
        # TODO: Fix this failing test
        # ctx_processor = 'openwisp2.context_processors.controller_api_settings'
        # super().test_notification_host_setting([ctx_processor])
        pass


class TestModels(BaseTestModels):
    app_label = 'sample_connection'


class TestModelsTransaction(BaseTestModelsTransaction):
    app_label = 'sample_connection'


class TestTasks(BaseTestTasks):
    pass


class TestSsh(BaseTestSsh):
    pass


class TestNotifications(BaseTestNotifications):
    app_label = 'sample_connection'


del BaseTestCommandInlines
del BaseTestConnectionAdmin
del BaseTestModels
del BaseTestModelsTransaction
del BaseTestSsh
del BaseTestTasks
del BaseTestNotifications
