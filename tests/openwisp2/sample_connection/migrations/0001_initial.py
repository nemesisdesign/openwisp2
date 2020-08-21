# Generated by Django 3.0.6 on 2020-05-10 18:11

import collections
import uuid

import django.db.models.deletion
import django.utils.timezone
import jsonfield.fields
import model_utils.fields
from django.db import migrations, models

import openwisp_controller.connection.base.models
import openwisp_users.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sample_config', '0001_initial'),
        ('openwisp_users', '0007_unique_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credentials',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    'created',
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='created',
                    ),
                ),
                (
                    'modified',
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='modified',
                    ),
                ),
                ('name', models.CharField(db_index=True, max_length=64, unique=True)),
                (
                    'connector',
                    models.CharField(
                        choices=[
                            ('openwisp_controller.connection.connectors.ssh.Ssh', 'SSH')
                        ],
                        db_index=True,
                        max_length=128,
                        verbose_name='connection type',
                    ),
                ),
                (
                    'params',
                    jsonfield.fields.JSONField(
                        default=dict,
                        dump_kwargs={'indent': 4},
                        help_text='global connection parameters',
                        load_kwargs={'object_pairs_hook': collections.OrderedDict},
                        verbose_name='parameters',
                    ),
                ),
                (
                    'auto_add',
                    models.BooleanField(
                        default=False,
                        help_text=(
                            'automatically add these credentials to the '
                            'devices of this organization; if no organization is '
                            'specified will be added to all the new devices'
                        ),
                        verbose_name='auto add',
                    ),
                ),
                ('details', models.CharField(blank=True, max_length=64, null=True)),
                (
                    'organization',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to='openwisp_users.Organization',
                        verbose_name='organization',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Access credentials',
                'verbose_name_plural': 'Access credentials',
                'abstract': False,
            },
            bases=(
                openwisp_controller.connection.base.models.ConnectorMixin,
                openwisp_users.mixins.ValidateOrgMixin,
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name='DeviceConnection',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    'created',
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='created',
                    ),
                ),
                (
                    'modified',
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='modified',
                    ),
                ),
                (
                    'update_strategy',
                    models.CharField(
                        blank=True,
                        choices=[
                            (
                                (
                                    'openwisp_controller.connection.connectors.'
                                    'openwrt.ssh.OpenWrt'
                                ),
                                'OpenWRT SSH',
                            )
                        ],
                        db_index=True,
                        help_text='leave blank to determine automatically',
                        max_length=128,
                        verbose_name='update strategy',
                    ),
                ),
                ('enabled', models.BooleanField(db_index=True, default=True)),
                (
                    'params',
                    jsonfield.fields.JSONField(
                        blank=True,
                        default=dict,
                        dump_kwargs={'indent': 4},
                        help_text=(
                            'local connection parameters (will override the '
                            'global parameters if specified)'
                        ),
                        load_kwargs={'object_pairs_hook': collections.OrderedDict},
                        verbose_name='parameters',
                    ),
                ),
                (
                    'is_working',
                    models.BooleanField(blank=True, default=None, null=True),
                ),
                (
                    'failure_reason',
                    models.CharField(
                        blank=True, max_length=128, verbose_name='reason of failure'
                    ),
                ),
                ('last_attempt', models.DateTimeField(blank=True, null=True)),
                ('details', models.CharField(blank=True, max_length=64, null=True)),
                (
                    'credentials',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='sample_connection.Credentials',
                    ),
                ),
                (
                    'device',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='sample_config.Device',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Device connection',
                'verbose_name_plural': 'Device connections',
                'abstract': False,
            },
            bases=(
                openwisp_controller.connection.base.models.ConnectorMixin,
                models.Model,
            ),
        ),
    ]
